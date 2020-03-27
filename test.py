import pandas as pd
import unittest


df = pd.read_csv("contestants.csv")

class TestStringMethods(unittest.TestCase):

    def run_test(self, year, country, place_final, points_final, place_sf, points_sf, points_tele_final=None, points_jury_final=None, points_tele_sf=None, points_jury_sf=None):
        sel = df[(df["year"] == year) & (df["to_country"] == country)]
        self.assertEqual(sel["points_final"].values[0], points_final)
        self.assertEqual(int(sel["place_final"].values[0]), place_final)

    def test_malta_2019(self):
        # https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2019
        year = 2019 
        country = "Malta"
        place_final = 14
        points_final = 107
        place_sf = 8
        points_sf = 157
        self.run_test(year, country, place_final, points_final, place_sf, points_sf)
        
    def test_greece_1989(self):
        # https://en.wikipedia.org/wiki/Eurovision_Song_Contest_1989
        year = 1989
        country = "Greece"
        points_final = 56
        place_final = 9
        place_sf = None
        points_sf = None
        self.run_test(year, country, place_final, points_final, place_sf, points_sf)

    def test_portugal_2017(self):
        # https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2017
        year = 2017
        country = "Portugal"
        place_final = 1
        place_sf = 1
        points_final = 758
        points_tele_final = 376
        points_jury_final = 382
        points_sf = 370
        points_tele_sf = 197
        points_jury_sf = 173
        self.run_test(year, country, place_final, points_final, place_sf, points_sf, points_tele_final, points_jury_final, points_tele_sf, points_jury_sf)

if __name__ == '__main__':
    unittest.main()