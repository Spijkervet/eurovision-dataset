from collections import defaultdict
from utils import cast_int
from contestant import Contestant
from country import Country
from utils import to_dict


class Contest:
    def __init__(self, year):
        self.year = year
        self.contestants = defaultdict(dict)
        self.countries = {}
        self.votes = {}

    def add_contestant_to_contest(self, contest_round, country, artist, song, page_url):
        contestant_key = "{}_{}_{}".format(self.year, country.name, artist)

        if contestant_key in self.contestants.keys():
            contestant = self.contestants[contest_round][contestant_key]
        else:
            contestant = Contestant(self.year, country, artist, song, page_url)
            self.contestants[contest_round][contestant_key] = contestant
        return contestant

    def add_country_to_contest(self, country_id, country_name):
        country = Country(country_name, country_id)
        self.countries[country_id] = country
        return country

    def get_country_name(self, country_id):
        return self.countries[country_id].name

    def get_vote(self, from_country, to_country):
        try:
            return self.votes[from_country][to_country]
        except Exception as e:
            print(e)
            pass
        return None

    def votes_to_list(self):
        l = []
        for contest_round, v in self.votes.items():
            for from_country, _countries in v.table.items():
                for to_country, points in _countries.items():
                    l.append(
                        [
                            self.year,
                            contest_round,
                            from_country,
                            to_country,
                            self.get_country_name(from_country),
                            self.get_country_name(to_country),
                            points[0],
                            points[1],
                            points[2],
                        ]
                    )
        return l

    def contestants_to_list(self):
        l = []
        for contest_round in self.contestants:
            for _, c in self.contestants[contest_round].items():
                l.append(
                    [
                        self.year,
                        c.country.code,
                        c.country.name,
                        c.performer,
                        c.song,
                        cast_int(c.place_contest),
                        cast_int(c.sf_num),
                        cast_int(c.running_final),
                        cast_int(c.running_sf),
                        cast_int(c.place_final),
                        cast_int(c.points_final),
                        cast_int(c.place_sf),
                        cast_int(c.points_sf),
                        cast_int(c.points_tele_final),
                        cast_int(c.points_jury_final),
                        cast_int(c.points_tele_sf),
                        cast_int(c.points_jury_sf),
                        ";".join(c.composers),
                        ";".join(c.lyricists),
                        c.lyrics,
                        c.youtube_url,
                    ]
                )
        return l

    def betting_offices_to_list(self):
        l = []
        for contest_round, contestant in self.contestants.items():
            for _, c in contestant.items():
                bos = to_dict(c.betting_offices, prepend_key="betting")
                country = to_dict(c.country, prepend_key="country")
                misc = {
                    "year": c.year,
                    "performer": c.performer,
                    "song": c.song,
                    "page_url": c.page_url,
                    "contest_round": contest_round,
                }
                misc.update(country)
                for b in bos:
                    b.update(misc)
                l.extend(bos)
        return l
