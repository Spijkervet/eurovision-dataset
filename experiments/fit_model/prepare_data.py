import os

import pandas as pd
import torch
import pickle
from torch.utils.data import TensorDataset
from tqdm import tqdm


def prepare_features(df):
    # fixes
    df.loc[df["year"] == "Azerbaijan_Running Scared_Ell", "year"] = 2011

    df["year"] = df["year"].astype(int)
    df = df[(df["year"] != 2020) & (df["year"] != 2023)]

    def feature_vec(row):
        feature_len = 512
        features = []
        for f in range(feature_len):
            features.append(row[str(f)])
        return features

    df["features"] = df.apply(feature_vec, axis=1)
    return df


def prepare_draws(df):
    draws = df.drop([".chain", ".iteration", ".draw"], axis=1)
    draws.columns = [
        col.replace("beta_contestant[", "").replace("]", "") for col in draws.columns
    ]
    draws = draws.T
    draws["stan_contestant"] = draws.index
    draws["stan_contestant"] = draws["stan_contestant"].astype(int)

    def draws_vec(row):
        draws = []
        n_draws = 4000
        for d in range(n_draws):
            draws.append(row[d])
        return draws

    draws["draws"] = draws.apply(draws_vec, axis=1)
    draws = draws[["draws", "stan_contestant"]]
    return draws


if __name__ == "__main__":
    DATA_DIR = "./data/draws_dataset/"
    os.makedirs(DATA_DIR, exist_ok=True)
    features = pd.read_csv("data/eurovision_tune_plus.csv", index_col="Unnamed: 0")
    features = prepare_features(features)

    stan_contestants = pd.read_csv("data/stan-contestants.csv")

    merged_df = pd.merge(
        features,
        stan_contestants,
        how="left",
        left_on=["year", "country"],
        right_on=["year", "country_name"],
    )

    merged_df = merged_df.dropna(subset=["stan_contestant"])

    # draws
    draws = pd.read_csv("data/contest-draws.csv")
    draws = prepare_draws(draws)
    merged_df = pd.merge(
        merged_df,
        draws,
        how="left",
        left_on="stan_contestant",
        right_on="stan_contestant",
    )
    print("Missing datapoints: {}".format(merged_df["stan_contestant"].isna().sum()))

    inputs = []
    targets = []
    for idx, row in tqdm(merged_df.iterrows(), total=merged_df.shape[0]):
        for draw in row["draws"]:
            inputs.append(row["features"])
            targets.append(draw)

    # Check if the above for loop made the correct mapping
    assert inputs[0] == merged_df.iloc[0]["features"]
    assert targets[0] == merged_df.iloc[0]["draws"][0]
    assert inputs[10] == merged_df.iloc[0]["features"]
    assert targets[10] == merged_df.iloc[0]["draws"][10]

    assert inputs[4000] == merged_df.iloc[1]["features"]
    assert targets[4000] == merged_df.iloc[1]["draws"][0]
    assert inputs[8005] == merged_df.iloc[2]["features"]
    assert targets[8005] == merged_df.iloc[2]["draws"][5]

    with open(os.path.join(DATA_DIR, "inputs.p"), "wb") as f:
        pickle.dump(inputs, f)

    with open(os.path.join(DATA_DIR, "targets.p"), "wb") as f:
        pickle.dump(targets, f)

    # for idx, (i, t) in enumerate(tqdm(zip(inputs, targets), total=len(inputs))):
    #     i = torch.tensor(i)
    #     t = torch.tensor(t)
    #     d = {"inputs": i, "targets": t}
    #     torch.save(d, os.path.join(DATA_DIR, f"{idx}.pt"))
