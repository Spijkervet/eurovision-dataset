from bs4 import BeautifulSoup
from copy import deepcopy
from .base import BaseScraper

class BettingOffice:
    def __init__(self, bm_id: int, sc_id: int, name: str):
        self.bm_id = bm_id
        self.sc_id = sc_id
        self.name = name
        self.score = None


class OddsScraper(BaseScraper):
    def __init__(self):
        super().__init__()

    def scrape_year(self, contest, contest_round):
        if contest_round == "final":
            url = "https://eurovisionworld.com/odds/eurovision-{}".format(contest.year)
        else:
            url = "https://eurovisionworld.com/odds/eurovision-{}-{}".format(
                contest.year, contest_round
            )

        self.driver.get(url)
        self.soup = BeautifulSoup(self.driver.page_source, features="html.parser")

        odds_table = self.soup.find("div", class_="odds_div")
        if odds_table is None:
            return contest

        betting_offices = []
        cols = odds_table.findAll("th")
        for c in cols:
            if c.has_attr("data-bm") and c.has_attr("data-sc"):
                bo = BettingOffice(
                    bm_id=int(c["data-bm"]), sc_id=int(c["data-sc"]), name=c.text
                )
                betting_offices.append(bo)

        rows = odds_table.find("tbody").findAll("tr")
        for row in rows:
            cols = row.findAll("td")

            if contest.year < 2017:
                place, country_artist_col = cols[:2]
                betting_cols = cols[2:]
            elif contest.year == 2017:
                place, historical_link, country_artist_col = cols[:3]
                betting_cols = cols[3:]
            elif contest.year > 2017:
                place, historical_link, country_artist_col, winning_chance = cols[:4]
                betting_cols = cols[4:]
            assert len(betting_cols) == len(betting_offices)

            # Add country to country dictionary
            country_name = country_artist_col.find_next(text=True).strip()
            country_id = country_name
            country = contest.add_country_to_contest(country_id, country_name)

            # Add contestant to contestant dictionary
            artist_song = country_artist_col.find("span").text
            artist, song = artist_song.split(" - ")
            page_url = country_artist_col.find("a")["href"]
            contestant = contest.add_contestant_to_contest(
                contest_round, country, artist, song, page_url
            )

            # add scores from all betting offices to contestant
            for bet_idx, score in enumerate(betting_cols):
                betting_office = deepcopy(betting_offices[bet_idx])

                score = score.text

                if score != "":
                    score = float(score)
                betting_office.score = score

                contestant.betting_offices.append(betting_office)
        return contest
