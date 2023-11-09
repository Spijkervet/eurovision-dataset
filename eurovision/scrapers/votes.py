from bs4 import BeautifulSoup
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
from collections import defaultdict

from contest import Contest
from country import Country
from votes import Votes

from .base import BaseScraper


class VotesScraper(BaseScraper):
    def __init__(self):
        super().__init__()

    def get_from_to_country_in_dict(self, from_country, to_country, d):
        if not d:
            return None

        for k, v in d.items():
            for _k, points in v.items():
                if k == from_country and _k == to_country:
                    return points
        return None

    def scrape_votes(self, contest, table_data_attrib=None):
        votes_dict = defaultdict(lambda: defaultdict(int))

        # Create the voting table for the contest
        voting_grid = self.soup.find("table", {"class": "scoreboard_table"})
        # with open("output1.html", "w") as file:
        #     file.write(str(self.soup))

        if voting_grid is None:
            return votes_dict

        if not voting_grid.contents:
            return votes_dict

        # Switch to other table for tele/jury voting
        if table_data_attrib:
            btn = WebDriverWait(self.driver, 20.0).until(
                EC.presence_of_element_located((By.CLASS_NAME, "scoreboard_button_div"))
            )

            btn = btn.find_element(
                By.XPATH, '//button[@data-button="{}"]'.format(table_data_attrib)
            )
            btn.send_keys(keys.Keys.SPACE)

            soup = BeautifulSoup(self.driver.page_source, features="html.parser")
            voting_grid = soup.find("table", {"class": "scoreboard_table"})

        if len(voting_grid.text) > 0:
            # Create country id/value pairs, since voting countries can be different than participating
            # countries (e.g. San Marino in 2007)
            countries = {}
            for row in voting_grid.find("thead").findAll("tr"):
                cols = row.find_all("td")
                for c in cols:
                    img = c.find("img")
                    if img:
                        countries[c["tdid"]] = img["alt"]

                    if "data-from" in c.attrs:
                        countries[c["data-from"]] = c["data-from"]

            for row in voting_grid.find("tbody").findAll("tr"):
                cols = row.find_all("td")
                country_name = cols[2].text
                country_id = cols[2]["data-to"]
                # total_points = cols[3].text

                points_cols = cols[4:]
                for p in points_cols:
                    if p.has_attr("data-from") and p.has_attr("data-to"):
                        from_country_id = p["data-from"]
                        to_country_id = p["data-to"]
                        if not p.text:
                            votes_dict[from_country_id][to_country_id] = 0
                        else:
                            votes_dict[from_country_id][to_country_id] = int(p.text)

                        from_country_name = countries[from_country_id]
                        to_country_name = countries[to_country_id]
                        contest.countries[from_country_id] = Country(
                            from_country_name, from_country_id
                        )
                        contest.countries[to_country_id] = Country(
                            to_country_name, to_country_id
                        )

        return votes_dict

    def get_contestants(self, contest: Contest, contest_round, rows, qualified=True):
        for row in rows:
            cols = row.find_all("td")

            # Tele/jury votes were implemented in 2016
            televotes = None
            juryvotes = None

            if len(cols) == 5:
                place_flag, country, song_artist, points, running = cols
            elif len(cols) == 7:
                (
                    place_flag,
                    country,
                    song_artist,
                    points,
                    televotes,
                    juryvotes,
                    running,
                ) = cols

            place = place_flag.find("b")
            if place is not None:
                place = place.text.rstrip()
                if not place.isdigit():
                    place = None

            country_name = country.text.rstrip(".")

            class_containing_country_id = place_flag.find("i")["class"][-1]
            country_id = class_containing_country_id.split("_", 1)[1]
            song = song_artist.find("a").text
            artist = song_artist.find("span").text.rstrip()
            song = song.replace(artist, "").rstrip()
            points = points.text.rstrip()
            running = running.text.rstrip()

            if not running.isdigit():
                running = None

            if country_name == "United KingdomUK":
                country_name = "United Kingdom"

            if country_name == "North MacedoniaNorth MacedoniaN.Macedonia":
                country_name = "North Macedonia"

            page_url = song_artist.find("a")["href"]

            if televotes and juryvotes:
                televotes = televotes["data-sort"].rstrip()
                juryvotes = juryvotes.text.rstrip()

            # Add country to country dictionary
            country = contest.add_country_to_contest(country_id, country_name)

            # Add contestant to contestant dictionary
            c = contest.add_contestant_to_contest(
                contest_round, country, artist, song, page_url
            )

            if qualified:
                if contest_round == "final":
                    c.running_final = running
                    c.place_contest = place  # place in contest = place in final
                    c.place_final = place
                    c.points_final = points
                    c.points_tele_final = televotes
                    c.points_jury_final = juryvotes
                else:
                    c.sf_num = self.get_sf_num(contest_round)
                    c.running_sf = running
                    c.place_sf = place
                    c.points_sf = points
                    c.points_tele_sf = televotes
                    c.points_jury_sf = juryvotes
            else:
                c.place_contest = place

            print(
                contest.year,
                c.country.name,
                contest_round if qualified else f"{contest_round} Non qualified",
            )
        return contest

    def scrape_year(self, contest, contest_round):
        if contest_round == "final":
            url = "https://eurovisionworld.com/eurovision/{}".format(contest.year)
        else:
            url = "https://eurovisionworld.com/eurovision/{}/{}".format(
                contest.year, contest_round
            )

        self.driver.get(url)
        self.soup = BeautifulSoup(self.driver.page_source, features="html.parser")
        voting_table = self.soup.find("div", {"id": "voting_table"})
        if not voting_table:
            return None

        # Qualified countries
        rows = voting_table.findAll("table")[0].find("tbody").findAll("tr")
        contest = self.get_contestants(contest, contest_round, rows)

        # Non-qualified countries, only for final ranking (place in contest)
        if len(voting_table.findAll("table")) > 1:
            rows = voting_table.findAll("table")[1].find("tbody").findAll("tr")
            contest = self.get_contestants(
                contest, contest_round, rows, qualified=False
            )

        # Tele/jury votes were implemented in 2016
        tele_votes = None
        jury_votes = None
        total_votes = self.scrape_votes(contest)
        if contest.year >= 2016:
            tele_votes = self.scrape_votes(contest, "tele")
            jury_votes = self.scrape_votes(contest, "jury")

        # Merge dictionaries:
        for k, v in total_votes.items():
            for _k, _v in v.items():
                tele_points = self.get_from_to_country_in_dict(k, _k, tele_votes)
                jury_points = self.get_from_to_country_in_dict(k, _k, jury_votes)
                total_votes[k][_k] = (_v, tele_points, jury_points)

        votes = Votes(contest.year, contest_round, total_votes)
        contest.votes[contest_round] = votes
        return contest

    def scrape_misc(self, contest):
        def get_items_for_contestant(contestant):
            url = "https://eurovisionworld.com" + contestant.page_url

            self.driver.get(url)
            soup = BeautifulSoup(self.driver.page_source, features="html.parser")

            # Get lyrics
            lyrics = soup.find("div", class_="lyrics_div")

            lyrics = "\\n\\n".join(
                [p.get_text(separator="\\n") for p in lyrics if p is not None]
            )

            contestant.lyrics = lyrics

            # Get video URL
            youtube_url = None
            video_wrapper = soup.find("div", class_="lyrics_video_wrap")
            if video_wrapper is not None:
                video_src = video_wrapper.find("iframe")["src"]
                video_id = video_src.split("/")[-1].split("?")[0]
                youtube_url = "https://youtube.com/watch?v=" + video_id
            contestant.youtube_url = youtube_url

            # Get composers (rewrite this...)
            tmp = []
            composers = soup.find("h4", class_="label", text=re.compile("COMPOSERS?"))
            if composers is None:
                composers = soup.find(
                    "h4", class_="label", text=re.compile("SONGWRITERS?")
                )
            if composers:
                composers = composers.parent.find("ul").find_all("li", recursive=False)
                tmp = []
                for c in composers:
                    tmp.append(c.find("b").text)
            contestant.composers = tmp

            lyricists = soup.find("h4", class_="label", text=re.compile("LYRICISTS?"))
            tmp = []
            if lyricists:
                lyricists = lyricists.parent.find("ul").find_all("li", recursive=False)
                tmp = []
                for c in lyricists:
                    tmp.append(c.find("b").text)
            contestant.lyricists = tmp
            return contestant

        max_attempts = 5
        for contest_round in contest.contestants:
            for _, contestant in contest.contestants[contest_round].items():
                n_attempts = 0
                while n_attempts < max_attempts:
                    try:
                        # Get contestant's page url
                        contestant = get_items_for_contestant(contestant)
                        break
                    except Exception as e:
                        print(f"Scraper is likely blocked by EurovisionWorld servers... (Attempt {n_attempts}/{max_attempts})")
                        print(e)
                        n_attempts += 1
                        time.sleep(5)  # to avoid getting temporarily blocked from scraping
        return contest
