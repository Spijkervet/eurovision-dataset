import pickle
import argparse

from data_reader import DataReader
from scraper import scrape_year
from eurovision import EuroVision

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Eurovision Data Scraper')
    parser.add_argument('--output', type=str, default='out.csv', help='Output file path (csv)')
    parser.add_argument('--start', type=int, default=1956, help='Start year range of the Eurovision Song Contest')
    parser.add_argument('--end', type=int, default=2019, help='End year range of the Eurovision Song Contest')
    args = parser.parse_args()

    all_entries = {}
    for y in range(args.start, args.end+1):
        print('Scraping: Eurovision Song Contest {}'.format(y))
        entries = scrape_year(y)
        if entries:
            all_entries.update(entries)

    ev = EuroVision(all_entries)
    ev.to_csv(args.output)
