import argparse
import os

import pandas as pd

from contest import Contest
from eurovision.scrapers import OddsScraper


def to_csv(contest):
    all_bets = contest.betting_offices_to_list()
    df = pd.DataFrame(all_bets)

    fn = "betting_offices.csv"
    if not os.path.exists(fn):
        df.to_csv(fn, index=False)
    else:
        df.to_csv(fn, mode="a", header=False, index=False)


def get_odds(y, rounds):
    contest = Contest(y)
    for r in rounds:
        print("Scraping: Eurovision Song Contest {} {}".format(y, r))
        contest = scraper.scrape_year(contest, r)
    return contest


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Eurovision Data Scraper")
    parser.add_argument(
        "--start",
        type=int,
        default=2015,
        help="Start year range of the Eurovision Song Contest",
    )
    parser.add_argument(
        "--end",
        type=int,
        default=2023,
        help="End year range of the Eurovision Song Contest",
    )
    args = parser.parse_args()

    if args.start < 2014:
        raise Exception("Odds are only calculated from 2015 onward")

    scraper = OddsScraper()
    rounds = ["final", "semi-final-1", "semi-final-2"]
    for y in range(args.start, args.end + 1):
        contest = get_odds(y, rounds)
        to_csv(contest)

    scraper.driver.quit()
