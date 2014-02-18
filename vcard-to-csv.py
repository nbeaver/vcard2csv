#!/usr/bin/env python
import vobject
import glob
import csv

#TODO It might be a good idea to make the output file configurable
csv_file = open("contacts.csv", 'w')
writer = csv.writer(csv_file, delimiter='\t') # Technically a tab-delimited file
writer.writerow(['Name','Telephone','Email','Note'])

for file in sorted(glob.glob("*.vcf")):
    name = telephone = email = note = ''
    print file
    vCard_text = open(file).read()
    vCard = vobject.readOne(vCard_text)
    vCard.validate()
    try:
        name = str(vCard.n.value).strip()
    except AttributeError:
        print "Could not find name for file ",file
        # A vCard without a name is not good.
        # It does not get a pass.
    try:
        telephone = str(vCard.tel.value).strip()
    except AttributeError:
        print "Could not find telephone number for file ",file
        pass # Missing phone number is worth mentioning, but not stopping for.
    try:
        email = str(vCard.email.value).strip()
    except AttributeError:
        pass # We don't expect every vCard to have an email address.
    try:
        note = str(vCard.note.value)
    except AttributeError:
        pass # Many vCards will not have a note.
    writer.writerow([name, telephone, email, note])
#else: # This is executed after the last run of the for loop
#    import code
#    code.interact(local=locals())
