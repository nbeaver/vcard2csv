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

def get_phone_numbers(vCard):
    cell = home = work = None
    for tel in vCard.tel_list:
        if vCard.version.value == '2.1':
            if 'CELL' in tel.singletonparams:
                cell = str(tel.value).strip()
            elif 'WORK' in tel.singletonparams:
                work = str(tel.value).strip()
            elif 'HOME' in tel.singletonparams:
                home = str(tel.value).strip()
            else:
                print "Warning: Unrecognized phone number category in file `"+file+"`"
                tel.prettyPrint()
        elif vCard.version.value == '3.0':
            if 'CELL' in tel.params['TYPE']:
                cell = str(tel.value).strip()
            elif 'WORK' in tel.params['TYPE']:
                work = str(tel.value).strip()
            elif 'HOME' in tel.params['TYPE']:
                home = str(tel.value).strip()
            else:
                print "Warning: Unrecognized phone number category in file `"+file+"`"
                tel.prettyPrint()
        else:
            raise NotImplementedError("Version not implemented:"+vCard.version.value)
    return cell, home, work

for file in vcards:
    name = full_name = cell = work = home = email = note = None
    vCard_text = open(file).read()
    vCard = vobject.readOne(vCard_text)
    vCard.validate()
    for key, val in vCard.contents.iteritems():
        if key == 'n':
            name = str(vCard.n.value).strip()
        elif key == 'fn':
            name = str(vCard.fn.value).strip()
        elif key == 'tel':
            cell, home, work = get_phone_numbers(vCard)
        elif key == 'email':
            email = str(vCard.email.value).strip()
        elif key == 'note':
            note = str(vCard.note.value)
        else:
            # An unused key, like `adr`, `title`, `url`, etc.
            pass
    if note == None:
        print "Warning: No name for file `"+file+"`"
    if all([cell, work, home]) == None:
        print "Warning: no telephone number for file `"+file+"` with name `"+name+"`"
    writer.writerow([name, cell, work, home, email, note])
#else: # This is executed after the last run of the for loop
#    import code
#    code.interact(local=locals())
