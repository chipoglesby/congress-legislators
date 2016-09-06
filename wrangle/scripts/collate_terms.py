import argparse
from csv import DictWriter
from loggy import loggy
from sys import stdout
import yaml

TERM_HEADERS = ['bioguide_id', 'state', 'office', 'party',
                'district', 'senate_class', 'start_date', 'end_date']

LOGGY = loggy('collate_terms')



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




if __name__ == '__main__':
    parser = argparse.ArgumentParser("Creates a simplified list of terms from the legislators files")
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='*')
    args = parser.parse_args()

    terms = []
    for inf in args.infile:
        LOGGY.info('Reading: %s' % inf.name)
        legislators = yaml.load(inf.read())
        LOGGY.info("Legislator count: %s" % len(legislators))
        for leg in legislators:
            bioguide_id = leg['id']['bioguide']
            for t in leg['terms']:
                term = extract_term_data(t)
                term['bioguide_id'] = bioguide_id
                terms.append(term)

    LOGGY.info("Terms counted: %s" % len(terms))

    csvout = DictWriter(stdout, fieldnames=TERM_HEADERS)
    csvout.writeheader()
    for term in sorted(terms, key=lambda t: (t['bioguide_id'], t['start_date'])):
        csvout.writerow(term)




