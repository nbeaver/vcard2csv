.PHONY: test-python3
test-python3 :
	python3 vcard2csv.py example-vcards/ contacts.tsv
	-python3 vcard2csv.py empty/ test.tsv

.PHONY: debug-python3
debug-python3 :
	python3 vcard2csv.py --debug example-vcards/ contacts.tsv
	-python3 vcard2csv.py --debug empty/ test.tsv

.PHONY: test-python2
test-python2 :
	python2 vcard2csv.py example-vcards/ contacts.tsv
	-python2 vcard2csv.py empty/ test.tsv

.PHONY: pip-install
pip-install: requirements.txt
	pip install -r requirements.txt
	# pip install vobject

.PHONY: pip-freeze
pip-freeze:
	pip freeze > requirements.txt

.PHONY: recreate-venv
recreate-venv: requirements.txt
	python3 -m venv .venv
	./.venv/bin/python -m pip install -r requirements.txt

.PHONY: install-in-venv
install-in-venv: ./.venv/bin/python
	./.venv/bin/python -m pip install .

.PHONY: format
format:
	black --quiet -- ./vcard2csv.py

.PHONY: pylint
pylint :
	pylint ./vcard2csv.py
