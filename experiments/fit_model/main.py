import os
import pickle

import lightning.pytorch as pl
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset, random_split


class DrawsDataset(Dataset):
    def __init__(self, root_dir: str):
        self.root_dir = root_dir

        with open(os.path.join(self.root_dir, "inputs.p"), "rb") as f:
            self.inputs = pickle.load(f)

        with open(os.path.join(self.root_dir, "targets.p"), "rb") as f:
            self.targets = pickle.load(f)

        self.total = len(self.inputs)

    def __len__(self):
        return self.total

    def __getitem__(self, idx):
        inputs = torch.tensor(self.inputs[idx], dtype=torch.float32)
        targets = torch.tensor(self.targets[idx], dtype=torch.float32)
        return inputs, targets


class DrawsModule(pl.LightningModule):
    def __init__(self, n_features: int, lr: float = 3e-4):
        super().__init__()
        self.save_hyperparameters()
        self.model = nn.Linear(n_features, 1)
        self.criterion = nn.MSELoss()

    def forward(self, x):
        return self.model(x)

    def step(self, batch):
        x, y = batch
        y_hat = self(x)
        return self.criterion(y_hat.squeeze(dim=1), y)

    def training_step(self, batch, batch_idx):
        loss = self.step(batch)
        self.log("loss/train", loss, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        loss = self.step(batch)
        self.log("loss/valid", loss, prog_bar=True)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.hparams.lr)


if __name__ == "__main__":
    batch_size = 512
    dataset = DrawsDataset(root_dir="./data/draws_dataset")

    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size

    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, num_workers=4, shuffle=True
    )
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, num_workers=4, shuffle=False
    )

    trainer = pl.Trainer(accelerator="auto", max_epochs=1)
    model = DrawsModule(n_features=512)

    trainer.fit(model, train_loader, val_loader)
