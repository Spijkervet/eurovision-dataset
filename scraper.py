from bs4 import BeautifulSoup
from selenium import webdriver
from collections import defaultdict

from country import Country
from contestant import Contestant
from votes import Votes

class Scraper():

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(chrome_options=options)


    def scrape_year(self, contest, contest_round):


        if contest_round == 'final':
            url = 'https://eurovisionworld.com/eurovision/{}'.format(contest.year)
        else:
            url = 'https://eurovisionworld.com/eurovision/{}/{}'.format(contest.year, contest_round)

        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, features='html.parser')

        voting_table = soup.find('div', {'id': 'voting_table'})
        if not voting_table:
            return None

        
        rows = voting_table.find('table').find('tbody').findAll('tr')
        for row in rows:
            cols = row.find_all('td')
            # Tele/jury votes were implemented in 2016
            televotes = None
            juryvotes = None
            if len(cols) == 6:
                place, flag, country, song_artist, points, running = cols
            if len(cols) == 8:
                place, flag, country, song_artist, points, televotes, juryvotes, running = cols

            place = place.text.rstrip()
            country_name = country.text.rstrip('.')
            country_id = flag.find('img')['alt'].rstrip()
            song = song_artist.find('a').text
            artist = song_artist.find('span').text.rstrip()
            song = song.replace(artist, '').rstrip()
            points = points.text.rstrip()
            running = running.text.rstrip()
            page_url = song_artist.find('a')['href']

            if televotes and juryvotes:
                televotes = televotes['data-sort'].rstrip()
                juryvotes = juryvotes.text.rstrip()

            # Add country to country dictionary
            country = Country(country_name, country_id)
            contest.countries[country_id] = country

            # Add contestant to contestant dictionary
            contestant_key = '{}_{}'.format(contest.year, country.name)

            if contestant_key in contest.contestants.keys():
                c = contest.contestants[contestant_key]
            else:
                c = Contestant(contest.year, country, artist, song, page_url)
                contest.contestants[contestant_key] = c

            if contest_round == 'final':
                c.running_final = running
                c.place_final = place
                c.points_final = points
                c.points_tele_final = televotes
                c.points_jury_final = juryvotes 
            elif contest_round == 'semi-final' or 'semi-final-1':
                c.running_sf1 = running
                c.place_sf1 = place
                c.points_sf1 = points
                c.points_tele_sf1 = televotes
                c.points_jury_sf1 = juryvotes 
            elif contest_round == 'semi-final-2':
                c.running_sf2 = running
                c.place_sf2 = place
                c.points_sf2 = points
                c.points_tele_sf2 = televotes
                c.points_jury_sf2 = juryvotes 

        # Create the voting table for the contest
        voting_grid = soup.find('div', {'id': 'voting_grid'})
        if len(voting_grid.text) > 0:
            voting_dict = defaultdict(lambda: defaultdict(int))

            # Create country id/value pairs, since voting countries can be different than participating
            # countries (e.g. San Marino in 2007)
            countries = {}
            for row in voting_grid.find('thead').findAll('tr'):
                cols = row.find_all('td')
                for c in cols:
                    img = c.find('img')
                    if img:
                        countries[c['tdid']] = img['alt']
            
            for row in voting_grid.find('tbody').findAll('tr'):
                cols = row.find_all('td')
                country_name = cols[2].text
                country_id = cols[2]['trid']
                # total_points = cols[3].text

                points_cols = cols[4:]
                for p in points_cols:
                    from_country_id = p['tdid']
                    to_country_id = p['trid']
                    if not p.text:
                        voting_dict[from_country_id][to_country_id] = 0
                    else:
                        voting_dict[from_country_id][to_country_id] = int(p.text)

                    from_country_name = countries[from_country_id]
                    to_country_name = countries[to_country_id]
                    contest.countries[from_country_id] = Country(from_country_name, from_country_id)
                    contest.countries[to_country_id] = Country(to_country_name, to_country_id)

                votes = Votes(contest.year, contest_round, voting_dict)
                contest.votes[contest_round] = votes

        return contest

    def scrape_misc(self, contest):
        for _, c in contest.contestants.items():

            country = c.country.name

            # Get contestant's page url
            url = 'https://eurovisionworld.com' + c.page_url

            print(url)

            self.driver.get(url)
            soup = BeautifulSoup(self.driver.page_source, features='html.parser')

            # Get lyrics
            lyrics = soup.find('div', class_='lyrics_div').findAll('p')
            lyrics = '\\n\\n'.join([p.get_text(separator='\\n') for p in lyrics])
            c.lyrics = lyrics

            # Get video URL 
            video_src = soup.find('div', class_='lyrics_video_wrap').find('iframe')['src']
            video_id = video_src.split('/')[-1].split('?')[0]
            youtube_url = 'https://youtube.com/watch?v=' + video_id
            c.youtube_url = youtube_url
        return contest