test :
	./vcard2csv.py example-vcards/ contacts.csv
	-./vcard2csv.py empty/ test.csv

requirements.txt :
	pipreqs .
