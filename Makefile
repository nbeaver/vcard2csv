test-python3 :
	python3 vcard2csv.py example-vcards/ contacts.tsv
	-python3 vcard2csv.py empty/ test.tsv

debug-python3 :
	python3 vcard2csv.py --debug example-vcards/ contacts.tsv
	-python3 vcard2csv.py --debug empty/ test.tsv

test-python2 :
	python2 vcard2csv.py example-vcards/ contacts.tsv
	-python2 vcard2csv.py empty/ test.tsv

requirements.txt : vcard2csv.py
	pipreqs --force .
