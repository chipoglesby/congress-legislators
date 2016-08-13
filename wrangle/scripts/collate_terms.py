from csv import DictWriter
from settings import FETCHED_DIR, COLLATED_DIR
import json

SRC_PATHS = FETCHED_DIR.glob('legislators-*.json')
DEST_PATH = COLLATED_DIR / 'legislators-terms.csv'

TERM_HEADERS = ['bioguide_id', 'state', 'office', 'party',
                'district', 'senate_class', 'start_date', 'end_date']

def extract_term_data(term):
    p = {}
    p['party'] = term.get('party')
    p['state'] = term['state']
    p['start_date'] = term['start']
    p['end_date'] = term['end']
    # Now figure out exact title...
    p['office'] = term['type']
    if  p['office'] == 'rep':
        p['district'] = term['district']
        p['senate_class'] = None
    elif p['office'] == 'sen':
        p['district'] = None
        p['senate_class'] = term['class']
    else:
        p['district'] = None
        p['senate_class'] = None
    return p

def extract_terms_data(terms):
    terms = datum['terms']


def main():
    destfile = DEST_PATH.open('w')
    destcsv = DictWriter(destfile, fieldnames=TERM_HEADERS)
    destcsv.writeheader()

    for srcpath in SRC_PATHS:
        legislators = json.loads(srcpath.read_text())
        for leg in legislators:
            bioguide_id = leg['id']['bioguide']
            for t in leg['terms']:
                term = extract_term_data(t)
                term['bioguide_id'] = bioguide_id
                destcsv.writerow(term)

    destfile.close()

if __name__ == '__main__':
    main()

