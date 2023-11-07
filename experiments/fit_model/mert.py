import pytorch_lightning as pl
import torch
import torch.nn as nn
from einops import rearrange
from transformers import AutoModel, Wav2Vec2FeatureExtractor

class Identity(nn.Module):

    def __init__(self):
        super().__init__()

    def forward(self, x):
        return x

class MERTModel(pl.LightningModule):
    def __init__(self, train_head: bool = False):
        super().__init__()
        self.train_head = train_head

        self.processor = Wav2Vec2FeatureExtractor.from_pretrained(
            "m-a-p/MERT-v1-330M", trust_remote_code=True
        )
        self.model = AutoModel.from_pretrained(
            "m-a-p/MERT-v1-330M", trust_remote_code=True
        )
        self.model = self.model.eval()

        if train_head:
            self.head = nn.Conv1d(in_channels=25, out_channels=1, kernel_size=1)
        else:
            self.head = Identity()

        self.sample_rate = 24000
        self.pretrain_context_sec = 5
        self.pretrain_context_samples = self.sample_rate * self.pretrain_context_sec

    def embed(self, audio: torch.Tensor) -> torch.Tensor:
        """Generates MERT embeddings from an audio tensor (sampled at 24kHz).
        MERT generates 25 representation layers (the last dimension). We can select the representation
        empirically, as each performs differently per downstream task, or learn an weighted average.
        More details at: https://huggingface.co/m-a-p/MERT-v1-330M

        Args:
            audio (torch.Tensor): Audio tensor

        Returns:
            torch.Tensor: MERT embeddings of shape (batch, sequence length, embedding dim, representation layer)
        """
        if audio.ndim == 2:
            audio = audio.unsqueeze(dim=1)

        inputs = self.processor(
            audio, sampling_rate=self.sample_rate, return_tensors="pt"
        )["input_values"]
        inputs = inputs[0].to(audio.device)
        hiddens = []
        for i in inputs.split(self.pretrain_context_samples, dim=2):
            with torch.no_grad():
                self.model = self.model.eval()
                h = torch.stack(
                    self.model(
                        i.squeeze(dim=1), output_hidden_states=True
                    ).hidden_states
                )
                n_embd = h.shape[-1]
                h = rearrange(h, "r b s n_embd -> b r (s n_embd)")

            h = self.head(h)
            hiddens.append(rearrange(h, "1 b (s n_embd) -> b s n_embd", n_embd=n_embd))
        hiddens = torch.cat(hiddens, dim=1)
        return hiddens

    def forward(self, audio: torch.Tensor) -> torch.Tensor:
        return self.embed(audio)
