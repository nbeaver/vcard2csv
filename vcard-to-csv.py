#!/usr/bin/env python
import vobject
import glob
import csv

csv_file = open("contacts.csv", 'w')
writer = csv.writer(csv_file, delimiter='\t')
writer.writerow(['Name','Telephone','Email','Note'])

for file in sorted(glob.glob("*.vcf")):
    name = ''
    telephone = ''
    email = ''
    note = ''
    print file
    vCard_text = open(file).read()
    vCard = vobject.readOne(vCard_text)
    vCard.validate()
    try:
        name = str(vCard.n.value).strip()
    except AttributeError:
        print "Could not find name for file ",file
        pass
    try:
        telephone = vCard.tel.value
    except AttributeError:
        print "Could not find telephone number for file ",file
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
#else:
#    import code
#    code.interact(local=locals())
