#!/usr/bin/env python
import vobject # to parse vCard (vcf) files
import glob # to open all *.vcf files
import csv
import sys

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

def get_info_list(file):
    name = cell = work = home = email = note = None
    vCard_text = open(file).read()
    vCard = vobject.readOne(vCard_text)
    vCard.validate()
    for key, val in vCard.contents.iteritems():
        if key == 'fn':
            name = vCard.fn.value
        elif key == 'n':
            if name is None:
                # May get overwritten if full name is available.
                name = str(vCard.n.valueRepr()).replace('  ', ' ').strip()
        elif key == 'tel':
            cell, home, work = get_phone_numbers(vCard)
        elif key == 'email':
            email = str(vCard.email.value).strip()
        elif key == 'note':
            note = str(vCard.note.value)
        else:
            # An unused key, like `adr`, `title`, `url`, etc.
            pass
    if name is None:
        print "Warning: no name for file `"+file+"`"
    if all(telephone_number is None for telephone_number in [cell, work, home]):
        print "Warning: no telephone number for file `"+file+"` with name `"+name+"`"

    return [name, cell, work, home, email, note]

if __name__ == "__main__":

    try:
        output_file_name = sys.argv[1]
    except IndexError:
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
        writer.writerow(get_info_list(file))
