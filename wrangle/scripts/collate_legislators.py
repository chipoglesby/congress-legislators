import argparse
from csv import DictWriter
from datetime import datetime
from loggy import loggy
from sys import stdout
import yaml

LOGGY = loggy('collate_legislators')

LEGISLATOR_HEADERS = [
    'bioguide_id',
    'full_name', 'party', 'office', 'state',
    'district', 'senate_class', 'state_rank',
    'terms_served', 'years_served', 'start_date', 'end_date',
    'first_name', 'middle_name', 'last_name',
    'birthdate', 'years_lived', 'gender', 'religion',
    'thomas_id', 'govtrack_id', 'opensecrets_id',
    'lis_id', 'votesmart_id', 'cspan_id',
    'icpsr_id', 'fec_ids', 'latest_fec_id',
    'updated_at'
]


def extract_biography(data, dateref):
    p = {}
    p['first_name'] = data['name']['first']
    p['last_name'] = data['name']['last']
    p['middle_name'] = data['name'].get('middle')

    p['full_name'] = data['name'].get('official_full') \
        or ' '.join([p[n] for n in ['first_name', 'middle_name', 'last_name'] if p.get(n)])
    # set the biography
    p['birthdate'] = data['bio'].get('birthday')
    if p['birthdate']:
        _dayslived = (dateref - datetime.strptime(p['birthdate'], '%Y-%m-%d')).days
        p['years_lived'] = round(_dayslived / 365, 1)
    else:
        p['years_lived'] = None
    p['gender'] = data['bio']['gender']
    p['religion'] = data['bio'].get('religion')
    return p

def extract_ids(data):
    ids = data['id']
    p = {'bioguide_id': ids['bioguide']}
    p['thomas_id'] = ids.get('thomas')
    p['govtrack_id'] = ids.get('govtrack')
    p['opensecrets_id'] = ids.get('opensecrets')
    p['icpsr_id'] = ids.get('icpsr')
    p['lis_id'] = ids.get('lis')
    p['votesmart_id'] = ids.get('votesmart')
    p['cspan_id'] = ids.get('cspan')

    if ids.get('fec'):
        p['fec_ids'] = ';'.join(ids['fec'])
        p['latest_fec_id'] = ids['fec'][0]

    return p


def extract_job(data, dateref):
    p = {}
    terms = data['terms']
    latest_term = terms[-1]
    latest_term_startdate = datetime.strptime(latest_term['start'], '%Y-%m-%d')
    p['start_date'] = datetime.strptime(terms[0]['start'], '%Y-%m-%d')
    p['end_date'] = datetime.strptime(latest_term['end'], '%Y-%m-%d')

    if latest_term_startdate > dateref:
        # probably should throw an error here...
        print("Warning: the reference time", dateref, "is *before* the start of this legislator's latest term:", latest_term_startdate)

    # derive party and role and tenure from terms
    p['party'] = latest_term.get('party')
    p['state'] = latest_term['state']

    # Now figure out exact title...
    p['office'] = latest_term['type']
    if  p['office'] == 'rep':
        p['district'] = latest_term['district']
        p['senate_class'] = None
        p['state_rank'] = None
    elif p['office'] == 'sen':
        p['district'] = None
        p['senate_class'] = latest_term['class']
        p['state_rank'] = latest_term.get('state_rank')
    else:
        p['district'] = None
        p['senate_class'] = None
        p['state_rank'] = None

    # Derive total number of days in office
    # to keep things simple, we'll include the latest term
    days_served = 0
    p['terms_served'] = 0
    for term in terms[0:-2]:
        p['terms_served'] += 1
        datex = datetime.strptime(term['start'], '%Y-%m-%d')
        datey = datetime.strptime(term['end'], '%Y-%m-%d')
        days_served += (datey - datex).days
        # manually calculate days served in current term
        days_served += (dateref - latest_term_startdate).days
        p['terms_served'] += 1
        p['years_served'] = round(days_served / 365, 2)

    return p




def main():
    today = datetime.now()

    destfile = DEST_PATH.open('w')
    destcsv = DictWriter(destfile, fieldnames=LEGISLATOR_HEADERS)
    destcsv.writeheader()

    for srcpath in SRC_PATHS:
        rows = json.loads(srcpath.read_text())
        for row in rows:
            legislator = {'updated_at': today.isoformat()}
            legislator.update(extract_ids(row))
            legislator.update(extract_biography(row, dateref=today))
            legislator.update(extract_job(row, dateref=today))
            destcsv.writerow(legislator)

    destfile.close()




if __name__ == '__main__':
    parser = argparse.ArgumentParser("Creates a simplified list of legislators from the legislators files")
    parser.add_argument('infile', type=argparse.FileType('r'), nargs='*')
    args = parser.parse_args()
    today = datetime.now()




    legislators = []
    for inf in args.infile:
        LOGGY.info('Reading: %s' % inf.name)
        rows = yaml.load(inf.read())
        LOGGY.info("Record count: %s" % len(rows))


        for row in rows:
            leg = {'updated_at': today.isoformat()}
            leg.update(extract_ids(row))
            leg.update(extract_biography(row, dateref=today))
            leg.update(extract_job(row, dateref=today))
            legislators.append(leg)

    csvout = DictWriter(stdout, fieldnames=LEGISLATOR_HEADERS)
    csvout.writeheader()
    for leg in sorted(legislators, key=lambda t: (t['bioguide_id'])):
        csvout.writerow(leg)





