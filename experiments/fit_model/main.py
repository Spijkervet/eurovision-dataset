import logging
import os
import pickle
import pandas as pd
import lightning.pytorch as pl
import torch
import torch.nn as nn
import torch.nn.functional as F
from lightning.pytorch.callbacks.early_stopping import EarlyStopping
from torch.utils.data import DataLoader, Dataset, random_split
from torchmetrics.functional import r2_score

logger = logging.getLogger(__name__)


class DrawsDataset(Dataset):
    def __init__(self, fp: str):
        dataset = pd.read_pickle(fp)
        self.inputs = dataset["inputs"].tolist()
        self.targets = dataset["targets"].tolist()

        assert len(self.inputs) == len(self.targets)
        self.total = len(self.inputs)

    def __len__(self):
        return self.total

    def __getitem__(self, idx):
        inputs = torch.tensor(self.inputs[idx], dtype=torch.float32)
        targets = torch.tensor(self.targets[idx], dtype=torch.float32)
        return inputs, targets


class DrawsModule(pl.LightningModule):
    def __init__(
        self,
        n_features: int,
        lr: float = 3e-6,
        weight_decay=1e-4,
    ):
        super().__init__()
        self.save_hyperparameters()
        self.model = nn.Sequential(
            nn.Linear(n_features, 1),
        )
        self.criterion = nn.MSELoss()

    def forward(self, x):
        return self.model(x)

    def step(self, batch):
        x, y = batch
        y_hat = self(x)
        y_hat = y_hat.squeeze(dim=1)
        loss = self.criterion(y_hat, y)
        return {"loss": loss, "l1": F.l1_loss(y_hat, y), "r2": r2_score(y_hat, y)}

    def training_step(self, batch, batch_idx):
        loss = self.step(batch)
        self.log("loss/train", loss["loss"], prog_bar=True)
        self.log("l1/train", loss["l1"], prog_bar=True)
        self.log("r2/train", loss["r2"], prog_bar=True)
        return loss["loss"]

    def validation_step(self, batch, batch_idx):
        loss = self.step(batch)
        self.log("loss/valid", loss["loss"], prog_bar=True)
        self.log("l1/valid", loss["l1"], prog_bar=True)
        self.log("r2/valid", loss["r2"], prog_bar=True)
        return loss["loss"]

    def configure_optimizers(self):
        return torch.optim.Adam(
            self.parameters(),
            lr=self.hparams.lr,
            weight_decay=self.hparams.weight_decay,
        )


if __name__ == "__main__":
    batch_size = 2048

    train_dataset = DrawsDataset("data/train.p")
    val_dataset = DrawsDataset("data/valid.p")

    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, num_workers=4, shuffle=True
    )
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, num_workers=4, shuffle=False
    )

    trainer = pl.Trainer(
        accelerator="auto",
        max_epochs=100,
        callbacks=[EarlyStopping(monitor="loss/valid", mode="min")],
    )
    model = DrawsModule(n_features=512)

    logger.warn(
        f"Train dataset: {len(train_dataset)}, Valid dataset: {len(val_dataset)}"
    )
    trainer.fit(model, train_loader, val_loader)
