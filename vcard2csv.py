#!/usr/bin/env python
import vobject # to parse vCard (vcf) files
import glob # to open all *.vcf files
import csv
import argparse
import os.path

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
                print "Warning: Unrecognized phone number category in `{}'".format(vCard)
                tel.prettyPrint()
        elif vCard.version.value == '3.0':
            if 'CELL' in tel.params['TYPE']:
                cell = str(tel.value).strip()
            elif 'WORK' in tel.params['TYPE']:
                work = str(tel.value).strip()
            elif 'HOME' in tel.params['TYPE']:
                home = str(tel.value).strip()
            else:
                printf "Warning: Unrecognized phone number category in `'".format(vCard)
                tel.prettyPrint()
        else:
            raise NotImplementedError("Version not implemented: {}".format(vCard.version.value))
    return cell, home, work

def get_info_list(vcard_filepath):
    name = cell = work = home = email = note = None
    with open(vcard_filepath) as fp:
        vCard_text = fp.read()
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
        print "Warning: no name for file `'".format(vcard_filepath)
    if all(telephone_number is None for telephone_number in [cell, work, home]):
        print "Warning: no telephone numbers for file `{}' with name `{}'".format(vcard_filepath, name)

    return [name, cell, work, home, email, note]

def readable_directory(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(
            'not an existing directory: {}'.format(path))
    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(
            'not a readable directory: {}'.format(path))
    return path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Combine a bunch of vCard (.vcf) files to TSV.'
    )
    parser.add_argument(
        'read_dir',
        type=readable_directory,
        help='Directory to read vCard files from.'
    )
    parser.add_argument(
        'tsv_file',
        type=argparse.FileType('w'),
        help='Output file',
    )
    args = parser.parse_args()
    vcard_pattern = os.path.join(args.read_dir, "*.vcf")

    vcards = sorted(glob.glob(vcard_pattern))

    if len(vcards) == 0:
        print "Error: no files ending with `.vcf` in directory `{}'".format(args.readable_directory)
        sys.exit(2)

    # Tab separated values are less annoying than comma-separated values.
    writer = csv.writer(args.tsv_file, delimiter='\t')
    writer.writerow(['Name','Cell phone','Work phone','Home phone','Email','Note'])

    for vcard in vcards:
        writer.writerow(get_info_list(vcard))
