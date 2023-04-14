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


def prepare_inputs_targets(data_dir):
    features = pd.read_csv(
        os.path.join(data_dir, "eurovision_tune_plus.csv"), index_col="Unnamed: 0"
    )
    features = prepare_features(features)

    stan_contestants = pd.read_csv(os.path.join(data_dir, "stan-contestants.csv"))

    merged_df = pd.merge(
        features,
        stan_contestants,
        how="left",
        left_on=["year", "country"],
        right_on=["year", "country_name"],
    )

    merged_df = merged_df.dropna(subset=["stan_contestant"])

    # draws
    draws = pd.read_csv(os.path.join(data_dir, "contest-draws.csv"))
    draws = prepare_draws(draws)
    merged_df = pd.merge(
        merged_df,
        draws,
        how="left",
        left_on="stan_contestant",
        right_on="stan_contestant",
    )
    print("Missing datapoints: {}".format(merged_df["stan_contestant"].isna().sum()))

    new_df = []
    for idx, row in tqdm(merged_df.iterrows(), total=merged_df.shape[0]):
        for draw in row["draws"]:
            d = {}

            d["inputs"] = row["features"]
            d["targets"] = draw
            d["year"] = row["year"]
            new_df.append(d)

    # Check if the above for loop made the correct mapping
    assert new_df[0]["inputs"] == merged_df.iloc[0]["features"]
    assert new_df[0]["targets"] == merged_df.iloc[0]["draws"][0]
    assert new_df[10]["inputs"] == merged_df.iloc[0]["features"]
    assert new_df[10]["targets"] == merged_df.iloc[0]["draws"][10]

    assert new_df[4000]["inputs"] == merged_df.iloc[1]["features"]
    assert new_df[4000]["targets"] == merged_df.iloc[1]["draws"][0]
    assert new_df[8005]["inputs"] == merged_df.iloc[2]["features"]
    assert new_df[8005]["targets"] == merged_df.iloc[2]["draws"][5]

    new_df = pd.DataFrame(new_df)
    years = new_df["year"].unique()

    valid_years = [1978, 1984, 1995, 2002, 2013, 2019]
    train_years = list(set(years) - set(valid_years))

    train_dataset = new_df[new_df["year"].isin(train_years)]
    valid_dataset = new_df[new_df["year"].isin(valid_years)]
    return train_dataset, valid_dataset


if __name__ == "__main__":
    data_dir = "data"
    train_dataset, valid_dataset = prepare_inputs_targets(data_dir)

    train_dataset.to_pickle(os.path.join(data_dir, "train.p"))
    valid_dataset.to_pickle(os.path.join(data_dir, "valid.p"))
