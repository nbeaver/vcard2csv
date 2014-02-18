#!/usr/bin/env python
import vobject
import glob
import csv

csv_file = open("contacts.csv", 'w')
writer = csv.writer(csv_file, delimiter='\t')
writer.writerow(['Name','Telephone','Email','Note'])

for file in glob.glob("*.vcf"):
    name = ''
    telephone = ''
    email = ''
    note = ''
    print file
    vCard_text = open(file).read()
    vCard = vobject.readOne(vCard_text)
    try:
        name = vCard.n.value
    except AttributeError:
        print "Could not find name"
        pass
    try:
        telelphone = vCard.tel.value
    except AttributeError:
        print "Could not find telephone number"
        pass
    try:
        email = vCard.email.value
    except AttributeError:
        pass
    try:
        note = vCard.note.value
    except AttributeError:
        pass
    writer.writerow([name, telephone, email, note])

else: # Last for loop iteration
    import code
    code.interact(local=locals())
