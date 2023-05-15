import argparse
import time

from contest import Contest
from eurovision.scrapers import VotesScraper
from utils import to_csv


def get_contest(scraper, y, rounds):
    contest = Contest(y)
    for r in rounds:
        print("Scraping: Eurovision Song Contest {} {}".format(y, r))
        contest = scraper.scrape_year(contest, r)

    contest = scraper.scrape_misc(contest, 'final')
    return contest


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Eurovision Data Scraper")
    parser.add_argument(
        "--start",
        type=int,
        default=1956,
        help="Start year range of the Eurovision Song Contest",
    )
    parser.add_argument(
        "--end",
        type=int,
        default=2020,
        help="End year range of the Eurovision Song Contest",
    )
    parser.add_argument(
        "--round-delay",
        type=float,
        default=1,
        help="Delay in seconds between round fetch.",
    )
    parser.add_argument(
        "--misc-delay",
        type=float,
        default=1,
        help="Delay in seconds between contestant details fetch.",
    )
    args = parser.parse_args()

    scraper = VotesScraper(args.round_delay, args.misc_delay)
    for y in range(args.start, args.end + 1):
        if y == 2020:  # Covid, no contest.
            continue
        if y < 2004:
            rounds = ["final"]
        elif y >= 2004 and y < 2008:
            rounds = ["final", "semi-final"]
        else:
            rounds = ["final", "semi-final-1", "semi-final-2"]

        contest = get_contest(scraper, y, rounds)
        for round in rounds:
            to_csv(contest, round)

    scraper.driver.quit()
