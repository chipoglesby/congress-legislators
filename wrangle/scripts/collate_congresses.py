import argparse
from csv import DictReader, DictWriter
from collections import defaultdict
from loggy import loggy
from sys import stdout

CONGRESS_HEADERS = ['congress', 'start_date', 'end_date']

LOGGY = loggy('loggy')


def extract_congresses(sessions):
    # first, condense all the congresses into a simple collection:

    # {'113': [('2013-01-03','2013-12-26'),
    #           ('2014-01-03', '2015-01-02')]
    # }
    data = defaultdict(list)
    for s in sessions:
        data[s['congress']].append((s['start'], s['end']))

    congresses = []
    for congress, sessions in sorted(data.items(), key=lambda x: int(x[0])):
        congresses.append({
                'congress': congress,
                'start_date': sessions[0][0],
                'end_date': sessions[-1][-1]
        })

    return congresses

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Creates a simplified list of congresses from the sessions file")
    parser.add_argument('infile', type=argparse.FileType('r'))
    args = parser.parse_args()
    infile = args.infile
    LOGGY.info('Reading: %s' % infile.name)
    records = list(DictReader(infile, delimiter='\t'))
    LOGGY.info("Row count: %s" % len(records))
    csvout = DictWriter(stdout, fieldnames=CONGRESS_HEADERS)
    csvout.writeheader()
    for row in extract_congresses(records):
        csvout.writerow(row)
