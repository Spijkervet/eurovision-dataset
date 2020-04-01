from collections import defaultdict
from utils import cast_int

class Contest():
    def __init__(self, year):
        self.year = year
        # self.round = contest_round
        self.contestants = {}
        self.countries = {}
        self.votes = {}

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
                    l.append([self.year, contest_round, from_country, to_country, self.get_country_name(
                        from_country), self.get_country_name(to_country), points[0], points[1], points[2]])
        return l

    def contestants_to_list(self):
        l = []
        for _, c in self.contestants.items():
            l.append([self.year, c.country.code,
                      c.country.name, c.performer, c.song,
                      cast_int(c.place_contest),
                      cast_int(c.sf_num),
                      cast_int(c.running_final), cast_int(c.running_sf),
                      cast_int(c.place_final), cast_int(c.points_final), cast_int(c.place_sf), cast_int(c.points_sf),
                      cast_int(c.points_tele_final), cast_int(c.points_jury_final), cast_int(c.points_tele_sf), cast_int(c.points_jury_sf),
                      ';'.join(c.composers), ';'.join(c.lyricists),
                      c.lyrics, c.youtube_url])
        return l
