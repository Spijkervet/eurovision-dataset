import pandas as pd

class DataReader(object):

    def __init__(self, fp):
        self.fp = fp

    def read(self):
        return pd.read_csv(self.fp)