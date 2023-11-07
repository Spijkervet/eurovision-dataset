import pandas as pd
import unittest


df = pd.read_csv("contestants.csv")


class TestStringMethods(unittest.TestCase):
    def run_test(
        self,
        year,
        country,
        song,
        performer,
        place_final,
        points_final,
        place_sf,
        points_sf,
        points_tele_final=None,
        points_jury_final=None,
        points_tele_sf=None,
        points_jury_sf=None,
    ):
        sel = df[(df["year"] == year) & (df["to_country"] == country)]

        self.assertEqual(sel["song"].values[0], song)
        self.assertEqual(sel["performer"].values[0], performer)

        if place_final is None:
            self.assertTrue(all(sel["place_final"].isna()))
        else:
            self.assertEqual(sel["place_final"].values[0], place_final)

        if points_final is None:
            self.assertTrue(all(sel["points_final"].isna()))
        else:
            self.assertEqual(int(sel["points_final"].values[0]), points_final)

        if place_sf is None:
            self.assertTrue(all(sel["place_sf"].isna()))
        else:
            self.assertEqual(int(sel["place_sf"].values[0]), place_sf)

        if points_sf is None:
            self.assertTrue(all(sel["points_sf"].isna()))
        else:
            self.assertEqual(int(sel["points_sf"].values[0]), points_sf)

        if points_tele_final is None:
            self.assertTrue(all(sel["points_tele_final"].isna()))
        else:
            self.assertEqual(int(sel["points_tele_final"].values[0]), points_tele_final)

        if points_jury_final is None:
            self.assertTrue(all(sel["points_jury_final"].isna()))
        else:
            self.assertEqual(int(sel["points_jury_final"].values[0]), points_jury_final)

        if points_tele_sf is None:
            self.assertTrue(all(sel["points_tele_sf"].isna()))
        else:
            self.assertEqual(int(sel["points_tele_sf"].values[0]), points_tele_sf)

        if points_jury_sf is None:
            self.assertTrue(all(sel["points_jury_sf"].isna()))
        else:
            self.assertEqual(int(sel["points_jury_sf"].values[0]), points_jury_sf)

    def test_malta_2019(self):
        # https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2019
        year = 2019
        country = "Malta"
        self.run_test(
            year=2019,
            country="Malta",
            song="Chameleon",
            performer="Michela Pace",
            place_final=14,
            points_final=107,
            place_sf=8,
            points_sf=157,
            points_tele_final=20,
            points_jury_final=87,
            points_tele_sf=50,
            points_jury_sf=107,
        )

    def test_greece_1989(self):
        # https://en.wikipedia.org/wiki/Eurovision_Song_Contest_1989
        self.run_test(
            year=1989,
            country="Greece",
            song="To Diko Sou Asteri",
            performer="Marianna",
            place_final=9,
            points_final=56,
            place_sf=None,
            points_sf=None,
        )

    def test_portugal_2017(self):
        # https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2017
        self.run_test(
            year=2017,
            country="Portugal",
            song="Amar Pelos Dois",
            performer="Salvador Sobral",
            place_final=1,
            points_final=758,
            place_sf=1,
            points_sf=370,
            points_tele_final=376,
            points_jury_final=382,
            points_tele_sf=197,
            points_jury_sf=173,
        )

    def test_ireland_2022(self):
        # https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2022
        self.run_test(
            year=2022,
            country="Ireland",
            song="That's Rich",
            performer="Brooke Scullion",
            place_final=None,
            points_final=None,
            place_sf=15,
            points_sf=47,
            points_tele_final=None,
            points_jury_final=None,
            points_tele_sf=35,
            points_jury_sf=12,
        )

    def test_switzerland_2022(self):
        # https://en.wikipedia.org/wiki/Eurovision_Song_Contest_2022
        self.run_test(
            year=2022,
            country="Switzerland",
            song="Boys Do Cry",
            performer="Marius Bear",
            place_final=17,
            points_final=78,
            place_sf=9,
            points_sf=118,
            points_tele_final=0,
            points_jury_final=78,
            points_tele_sf=11,
            points_jury_sf=107,
        )

    def test_sweden_1959(self):
        # https://en.wikipedia.org/wiki/Eurovision_Song_Contest_1959
        self.run_test(
            year=1959,
            country="Sweden",
            song="Augustin",
            performer="Brita Borg",
            place_final=9,
            points_final=4,
            place_sf=None,
            points_sf=None,
            points_tele_final=None,
            points_jury_final=None,
            points_tele_sf=None,
            points_jury_sf=None,
        )

    def test_belgium_1959(self):
        # https://en.wikipedia.org/wiki/Eurovision_Song_Contest_1959
        self.run_test(
            year=1959,
            country="Belgium",
            song="Hou Toch Van Mij",
            performer="Bob Benny",
            place_final=6,
            points_final=9,
            place_sf=None,
            points_sf=None,
            points_tele_final=None,
            points_jury_final=None,
            points_tele_sf=None,
            points_jury_sf=None,
        )


if __name__ == "__main__":
    unittest.main()
