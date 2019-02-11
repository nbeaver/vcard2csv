#!/usr/bin/env python
import vobject
import glob
import csv
import argparse
import os.path
import sys
import logging
import collections

column_order = [
    'Name',
    'Cell phone',
    'Work phone',
    'Home phone',
    'Email',
    'Note',
]

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
                logging.warning("Warning: Unrecognized phone number category in `{}'".format(vCard))
                tel.prettyPrint()
        elif vCard.version.value == '3.0':
            if 'CELL' in tel.params['TYPE']:
                cell = str(tel.value).strip()
            elif 'WORK' in tel.params['TYPE']:
                work = str(tel.value).strip()
            elif 'HOME' in tel.params['TYPE']:
                home = str(tel.value).strip()
            else:
                logging.warning("Unrecognized phone number category in `{}'".format(vCard))
                tel.prettyPrint()
        else:
            raise NotImplementedError("Version not implemented: {}".format(vCard.version.value))
    return cell, home, work

def get_info_list(vcard_filepath):
    vcard = collections.OrderedDict()
    for column in column_order:
        vcard[column] = None
    name = cell = work = home = email = note = None
    with open(vcard_filepath) as fp:
        vCard_text = fp.read()
    vCard = vobject.readOne(vCard_text)
    vCard.validate()
    for key, val in vCard.contents.iteritems():
        if key == 'fn':
            name = vCard.fn.value
            vcard['Name'] = name
        elif key == 'n':
            if name is None:
                # May get overwritten if full name is available.
                name = str(vCard.n.valueRepr()).replace('  ', ' ').strip()
                vcard['Name'] = name

                # TODO: separate fields for name and full name.
        elif key == 'tel':
            cell, home, work = get_phone_numbers(vCard)
            vcard['Cell phone'] = cell
            vcard['Home phone'] = home
            vcard['Work phone'] = work
        elif key == 'email':
            email = str(vCard.email.value).strip()
            vcard['Email'] = email
        elif key == 'note':
            note = str(vCard.note.value)
            vcard['Note'] = note
        else:
            # An unused key, like `adr`, `title`, `url`, etc.
            pass
    if name is None:
        logging.warning("no name for file `{}'".format(vcard_filepath))
    if all(telephone_number is None for telephone_number in [cell, work, home]):
        logging.warning("no telephone numbers for file `{}' with name `{}'".format(vcard_filepath, name))

    return vcard

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
        description='Convert a bunch of vCard (.vcf) files to a single TSV file.'
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
    parser.add_argument(
        '-v',
        '--verbose',
        help='More verbose logging',
        dest="loglevel",
        default=logging.WARNING,
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        '-d',
        '--debug',
        help='Enable debugging logs',
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    vcard_pattern = os.path.join(args.read_dir, "*.vcf")
    vcards = sorted(glob.glob(vcard_pattern))
    if len(vcards) == 0:
        logging.error("no files ending with `.vcf` in directory `{}'".format(args.read_dir))
        sys.exit(2)

    # Tab separated values are less annoying than comma-separated values.
    writer = csv.writer(args.tsv_file, delimiter='\t')
    writer.writerow(column_order)

    for vcard_path in vcards:
        vcard_info = get_info_list(vcard_path)
        writer.writerow(vcard_info.values())
