from settings import FETCHED_DIR, COLLATED_DIR
from csv import DictReader, DictWriter
from collections import defaultdict

SRC_PATH = FETCHED_DIR / 'sessions.csv'
DEST_PATH = COLLATED_DIR / 'congresses.csv'

CONGRESS_HEADERS = ['congress', 'start_date', 'end_date']

def main():
    # first, condense all the congresses into a simple collection:

    # {'113': [('2013-01-03','2013-12-26'),
    #           ('2014-01-03', '2015-01-02')]
    # }
    congresses = defaultdict(list)
    for s in DictReader(SRC_PATH.read_text().splitlines()):
        congresses[s['congress']].append((s['start'], s['end']))

    with DEST_PATH.open('w') as df:
        destcsv = DictWriter(df, fieldnames=CONGRESS_HEADERS)
        destcsv.writeheader()
        for congress, sessions in sorted(congresses.items(), key=lambda x: int(x[0])):
            destcsv.writerow({
                    'congress': congress,
                    'start_date': sessions[0][0],
                    'end_date': sessions[-1][-1]
            })
        # the end


if __name__ == '__main__':
    main();


