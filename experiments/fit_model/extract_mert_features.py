import os
import pickle
from glob import glob

import pandas as pd
import torchaudio
from experiments.fit_model.mert import MERTModel
from tqdm import tqdm

if __name__ == "__main__":
    mert = MERTModel()
    mert = mert.to("cuda")

    fps = glob("./data/24k/**/*.mp3")
    data = []
    for idx, fp in enumerate(tqdm(fps)):
        mert_fp = f"./mert_features/{idx}.p"

        if os.path.exists(mert_fp):
            continue

        audio, sr = torchaudio.load(fp)
        assert sr == 24000  # 24khz
        assert audio.shape[0] == 1  # mono

        audio = audio.to(mert.device)
        try:
            features = mert(audio)
        except Exception as e:
            print(e)
            continue
        
        features = features.mean(dim=1)  # mean on the batch
        features = features.mean(dim=0)  # mean on the features

        year = int(fp.split("/")[-2])
        country = fp.split("/")[-1].split("_", 1)[0]

        d = {"year": year, "country": country, "features": features.cpu().numpy()}
        data.append(d)

        with open(mert_fp, "wb") as f:
            pickle.dump(d, f)

    df = pd.DataFrame(data)
    df.to_pickle("mert_features.p")
