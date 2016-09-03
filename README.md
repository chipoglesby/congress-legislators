# U.S. Congress Legislators and Terms in Office

Three tables:

- congress-legislators.csv - biographical information about each legislator, including latest term in office.
- congress-legislators-terms.csv - A record for each term in office per legislator.
- congresses.csv - A listing of Congresses (i.e. their number, from 1 to 114) and their start and end dates.


Sources:

- data/us/sessions.tsv from govtrack: https://www.govtrack.us/developers/data
- legislators-current.yaml from https://github.com/unitedstates/congress-legislators
- legislators-historical.yaml from https://github.com/unitedstates/congress-legislators


# Makefile

Run `./make` to fetch and collate the data in the wrangle/corral stash.
testing
