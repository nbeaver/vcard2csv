#!/usr/bin/env python
import vobject # to parse vCard (vcf) files
import glob # to open all *.vcf files
import csv
import sys

if len(sys.argv) > 1:
    output_file_name = sys.argv[1]
else:
    print "Usage: vcard-to-csv.py foo.csv"
    sys.exit(1)

vcards = sorted(glob.glob("*.vcf"))

if len(vcards) == 0:
    print "Error: no files ending with `.vcf` in current directory."
    sys.exit(2)

csv_file = open(output_file_name, 'w')

# Tab separated values are less annoying than comma-separated values.
writer = csv.writer(csv_file, delimiter='\t')
writer.writerow(['Name','Cell phone','Work phone','Home phone','Email','Note'])

for file in vcards:
    name = cell = work = home = email = note = ''
    vCard_text = open(file).read()
    vCard = vobject.readOne(vCard_text)
    vCard.validate()
    if vCard.version.value == '3.0':
        print "Warning: cannot process file `"+file+"` because it is vCard version 3.0."
        continue
    try:
        name = str(vCard.n.value).strip()
    except AttributeError:
        print "Error: No name for file ",file
        vCard.prettyPrint() 
        # A vCard without a name is not good,
        # so we let the exception crash the script.
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
                print "Warning: Unrecognized phone number category:",str(tel.singletonparams),' for phone number ',tel.value, tel,'in file `'+file+'`'
    except AttributeError:
        print "Warning: no telephone number for file `"+file+"` with name `"+name+"`"
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
