from settings import FETCHED_DIR
import csv
import requests
SRC_URL = 'https://www.govtrack.us/data/us/sessions.tsv'
DEST_PATH = FETCHED_DIR / 'sessions.csv'


def main():
    resp = requests.get(SRC_URL)

    with DEST_PATH.open('w') as df:
        destcsv = csv.writer(df)
        for row in csv.reader(resp.text.splitlines(), delimiter='\t'):
            destcsv.writerow(row)


if __name__ == '__main__':
    main();


