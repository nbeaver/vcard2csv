test :
	./vcard2csv.py example-vcards/ contacts.tsv
	-./vcard2csv.py empty/ test.tsv

requirements.txt :
	pipreqs .
