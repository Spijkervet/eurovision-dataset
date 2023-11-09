import argparse
import time
from contest import Contest
from eurovision.scrapers import VotesScraper
from utils import to_csv


def get_contest(y, rounds, max_attempts: int = 5):
    contest = None
    n_attempts = 0
    while contest is None:
        if n_attempts > max_attempts:
            raise Exception(f"Could not scrape {y} {rounds} in {n_attempts} attempts")

        try:
            contest = Contest(y)
            for r in rounds:
                print(
                    f"Scraping: Eurovision Song Contest {y} {r} (attempt {n_attempts}/{max_attempts})"
                )
                contest = scraper.scrape_year(contest, r)

            if contest is None:
                time.sleep(5)

        except Exception as e:
            print(f"Failed {y} {r} (attempt {n_attempts}/{max_attempts})")
            print(e)
            time.sleep(5)
        n_attempts += 1

    contest = scraper.scrape_misc(contest)
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
        default=2023,
        help="End year range of the Eurovision Song Contest",
    )
    args = parser.parse_args()

    scraper = VotesScraper()
    for y in range(args.start, args.end + 1):
        if y < 2004:
            rounds = ["final"]
        elif y >= 2004 and y < 2008:
            rounds = ["final", "semi-final"]
        else:
            rounds = ["final", "semi-final-1", "semi-final-2"]

        contest = get_contest(y, rounds)
        to_csv(contest)

    scraper.driver.quit()
