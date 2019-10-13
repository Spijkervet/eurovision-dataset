import pandas as pd

class EuroVision():

    def __init__(self, entries):
        self.entries = entries

    def to_csv(self, out_fp):
        d = {}
        for k, v in self.entries.items():
            d[k] = v.__dict__
        df = pd.DataFrame.from_dict(d, orient="index")
        df.to_csv(out_fp)