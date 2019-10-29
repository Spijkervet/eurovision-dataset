import pickle
import argparse
import pandas as pd

from scraper import Scraper
from utils import to_csv

from contest import Contest


def get_contests(start, end):
    contests = []
    for y in range(args.start, args.end+1):
        if y < 2004:
            rounds = ['final']
        elif y >= 2004 and y < 2008:
            rounds = ['final', 'semi-final']
        else:
            rounds = ['final', 'semi-final-1', 'semi-final-2']
        
        contest = Contest(y)
        for r in rounds:
            print('Scraping: Eurovision Song Contest {} {}'.format(y, r))
            contest = scraper.scrape_year(contest, r)
        
        contest = scraper.scrape_misc(contest)
        contests.append(contest)
    return contests

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Eurovision Data Scraper')
    parser.add_argument('--start', type=int, default=1956,
                        help='Start year range of the Eurovision Song Contest')
    parser.add_argument('--end', type=int, default=2019,
                        help='End year range of the Eurovision Song Contest')
    args = parser.parse_args()

    scraper = Scraper()
    contests = get_contests(args.start, args.end)
    to_csv(contests)