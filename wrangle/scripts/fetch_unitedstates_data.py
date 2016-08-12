from settings import FETCHED_DIR
from sys import argv
import json
import requests
import yaml

SRC_URL_DIR = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/master/'
DEFAULT_FILESTEMS = [
    'legislators-current',
    'legislators-historical',
]


def main():
    filestems = argv[1:] if len(argv) > 1 else DEFAULT_FILESTEMS
    print("Fetching:", '\n\t-'.join(filestems))
    for fstem in filestems:
        src_url = SRC_URL_DIR + fstem + '.yaml'
        dest_path = FETCHED_DIR / (fstem + '.json')
        print("Downloading\n\t:", src_url)
        resp = requests.get(src_url)
        if resp.status_code == 200:
            print("Saving:\n\t", dest_path)
            ydata = yaml.load(resp.text)
            dest_path.write_text(json.dumps(ydata, indent=2))

        else:
            raise "Status code was %s" % resp.status_code




if __name__ == '__main__':
    main();
