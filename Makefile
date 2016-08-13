WRANGLE_DIR=./wrangle
SCRIPTS_DIR=$(WRANGLE_DIR)/scripts
FETCHED_DIR=$(WRANGLE_DIR)/corral/fetched
COLLATED_DIR=$(WRANGLE_DIR)/corral/collated
DATA_DIR=./data
SAMPLES_DIR=$(DATA_DIR)/samples

all: fetch collate

fetch: $(FETCHED_DIR)/sessions.csv\
		$(FETCHED_DIR)/legislators-current.json\
		$(FETCHED_DIR)/legislators-historical.json

$(FETCHED_DIR)/sessions.csv:
	python $(SCRIPTS_DIR)/fetch_sessions.py

$(FETCHED_DIR)/legislators-current.json:
	python $(SCRIPTS_DIR)/fetch_unitedstates_legislators.py legislators-current

$(FETCHED_DIR)/legislators-historical.json:
	python $(SCRIPTS_DIR)/fetch_unitedstates_legislators.py legislators-historical


collate: $(COLLATED_DIR)/legislators.csv\
		 $(COLLATED_DIR)/terms.csv\
		 $(COLLATED_DIR)/congresses.csv

$(COLLATED_DIR)/legislators.csv:
	python $(SCRIPTS_DIR)/collate_legislators.py

$(COLLATED_DIR)/terms.csv:
	python $(SCRIPTS_DIR)/collate_terms.py

$(COLLATED_DIR)/congresses.csv:
	python $(SCRIPTS_DIR)/collate_congresses.py



package_data:
	mkdir -p $(DATA_DIR)
	cp $(COLLATED_DIR)/congresses.csv $(DATA_DIR)/congresses.csv
	# cp $(COLLATED_DIR)/legislators.csv $(DATA_DIR)/congress-legislators.csv
	# cp $(COLLATED_DIR)/terms.csv $(DATA_DIR)/congress-legislators-terms.csv

package_samples:
	mkdir -p $(SAMPLES_DIR)
	cp $(FETCHED_DIR)/legislators-current.json $(SAMPLES_DIR)/legislators-current.json
	cp $(FETCHED_DIR)/sessions.csv $(SAMPLES_DIR)/sessions.csv


clean:
	rm -r wrangle/corral

clean_collate:
	rm -rf $(COLLATED_DIR)
	mkdir -p $(COLLATED_DIR)
	@$(MAKE) $(THIS_FILE) collate
