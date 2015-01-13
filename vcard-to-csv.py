#!/usr/bin/env python
import vobject # to parse vCard (vcf) files
import glob # to open all *.vcf files
import csv
import sys

#DONE Take output name as argument.
output_file_name = sys.argv[1]
csv_file = open(output_file_name, 'w')
# Tab separated values are less annoying than comma-separated values.
writer = csv.writer(csv_file, delimiter='\t')
writer.writerow(['Name','Cell phone','Work phone','Home phone','Email','Note'])

for file in sorted(glob.glob("*.vcf")):
    name = cell = work = home = email = note = ''
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
        for tel in vCard.tel_list:
            # This strategy limits this to version 2.1 vCards.
            # We would need to parse e.g. type=CELL for version 3.0 vCards.
            if 'CELL' in tel.singletonparams:
                cell = str(tel.value).strip()
            elif 'WORK' in tel.singletonparams:
                work = str(tel.value).strip()
            elif 'HOME' in tel.singletonparams:
                home = str(tel.value).strip()
            else:
                print "Unrecognized phone number category:",str(tel.singletonparams),' for phone number ',tel.value, tel
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
    writer.writerow([name, cell, work, home, email, note])
#else: # This is executed after the last run of the for loop
#    import code
#    code.interact(local=locals())
