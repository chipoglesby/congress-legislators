from pathlib import Path

CORRAL_DIR = Path('wrangle', 'corral')
FETCHED_DIR = CORRAL_DIR / 'fetched'
COLLATED_DIR = CORRAL_DIR / 'collated'

for d in [FETCHED_DIR, COLLATED_DIR]:
    d.mkdir(exist_ok=True, parents=True)
