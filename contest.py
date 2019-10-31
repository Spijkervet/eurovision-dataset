from collections import defaultdict


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
                      c.sf_num,
                      c.running_final, c.running_sf,
                      c.place_final, c.points_final, c.place_sf, c.points_sf,
                      c.points_tele_final, c.points_jury_final, c.points_tele_sf, c.points_jury_sf,
                      ';'.join(c.composers), ';'.join(c.lyricists),
                      c.lyrics, c.youtube_url])
        return l
