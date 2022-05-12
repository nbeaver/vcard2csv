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
    'First name',
    'Last name',
    'Cell phone',
    'Work phone',
    'Home phone',
    'Mobile phone',
    'Email',
    'Address',
    'Note',
    'Birthday',
]

def get_phone_numbers(vCard):
    cell = home = work = mobile = None
    for tel in vCard.tel_list:
        if vCard.version.value == '2.1':
            if 'CELL' in tel.singletonparams:
                cell = str(tel.value).strip()
            elif 'WORK' in tel.singletonparams:
                work = str(tel.value).strip()
            elif 'HOME' in tel.singletonparams:
                home = str(tel.value).strip()
            elif 'MOBILE' in tel.singletonparams:
                mobile = str(tel.value).strip()
            else:
                logging.warning("Warning: Unrecognized phone number category in `{}'".format(vCard))
                tel.prettyPrint()
        elif vCard.version.value == '3.0':
            if 'CELL' in tel.params['TYPE'] or 'cell' in tel.params['TYPE']:
                cell = str(tel.value).strip()
            elif 'WORK' in tel.params['TYPE'] or 'work' in tel.params['TYPE']:
                work = str(tel.value).strip()
            elif 'HOME' in tel.params['TYPE'] or 'home' in tel.params['TYPE']:
                home = str(tel.value).strip()
            elif 'mobile' in tel.params['TYPE'] or 'MOBILE' in tel.params['TYPE']:
                mobile = str(tel.value).strip()
            else:
                logging.warning("Unrecognized phone number category in `{}'".format(vCard))
                tel.prettyPrint()
        else:
            raise NotImplementedError("Version not implemented: {}".format(vCard.version.value))
    return cell, home, work, mobile

def get_info_list(vCard, vcard_filepath):
    vcard = collections.OrderedDict()
    for column in column_order:
        vcard[column] = None
    name = cell = work = home = mobile = None
    vCard.validate()
    for key, val in list(vCard.contents.items()):
        if key == 'fn':
            vcard['Name'] = vCard.fn.value
            names = vCard.fn.value.split(' ')
            vcard['First name'] = names[0]
            vcard['Last name'] = names[1]
        elif key == 'n':
            name = str(vCard.n.valueRepr()).replace('  ', ' ').strip()
            vcard['Name'] = name
            names = name.split(' ')
            vcard['First name'] = names[0]
            vcard['Last name'] = names[1]
        elif key == 'tel':
            cell, home, work, mobile = get_phone_numbers(vCard)
            vcard['Cell phone'] = cell
            vcard['Home phone'] = home
            vcard['Work phone'] = work
            vcard['Mobile phone'] = mobile
        elif key == 'email':
            email = str(vCard.email.value).strip()
            vcard['Email'] = email
        elif key == 'note':
            note = str(vCard.note.value)
            vcard['Note'] = note
        elif key == 'adr':
            adr = str(vCard.adr.value).strip()
            if adr.startswith('"') and adr.endswith('"'):
                adr = adr[1:-1]
            vcard['Address'] = adr
        elif key == 'bday':
            bday = str(vCard.bday.value).strip()
            vcard['Birthday'] = bday
        elif key == 'version':
            # Ignore the key for vcard version
            pass
        else:
            print('unidentified key ' + key)
            # An unused key, like `adr`, `title`, `url`, etc.
            pass
    if name is None:
        logging.warning("no name for vCard in file `{}'".format(vcard_filepath))
    if all(telephone_number is None for telephone_number in [cell, work, home, mobile]):
        logging.warning("no telephone numbers for file `{}' with name `{}'".format(vcard_filepath, name))

    return vcard

def get_vcards(vcard_filepath):
    with open(vcard_filepath) as fp:
        all_text = fp.read()
    for vCard in vobject.readComponents(all_text):
        yield vCard


def readable_directory(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(
            'not an existing directory: {}'.format(path))
    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(
            'not a readable directory: {}'.format(path))
    return path

def writable_file(path):
    if os.path.exists(path):
        if not os.access(path, os.W_OK):
            raise argparse.ArgumentTypeError(
                'not a writable file: {}'.format(path))
    else:
        # If the file doesn't already exist,
        # the most direct way to tell if it's writable
        # is to try writing to it.
        with open(path, 'w') as fp:
            pass
    return path

def main():
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
        type=writable_file,
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
    parser.add_argument(
        '-r',
        '--recursive',
        help='Recursively search for vcard files in the specified directory & subdirectories',
        action='store_true',
        dest='is_recursive'
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    if args.is_recursive:
        vcard_pattern = os.path.join(args.read_dir, "**/*.vcf")
    else:
        vcard_pattern = os.path.join(args.read_dir, "*.vcf")
    vcard_paths = sorted(glob.glob(vcard_pattern, recursive=args.is_recursive))
    if len(vcard_paths) == 0:
        logging.error("no files ending with `.vcf` in directory `{}'".format(args.read_dir))
        sys.exit(2)

    # Tab separated values are less annoying than comma-separated values.
    with open(args.tsv_file, 'w') as tsv_fp:
        writer = csv.writer(tsv_fp, delimiter='\t')
        writer.writerow(column_order)

        for vcard_path in vcard_paths:
            for vcard in get_vcards(vcard_path):
                vcard_info = get_info_list(vcard, vcard_path)
                writer.writerow(list(vcard_info.values()))

if __name__ == "__main__":
    main()
