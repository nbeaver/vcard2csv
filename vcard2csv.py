#! /usr/bin/env python3
import glob
import csv
import argparse
import os.path
import logging
import collections
import vobject

logger = logging.getLogger(__name__)

column_order = [
    "Formatted Name",
    "Name",
    "Prefix",
    "Given name",
    "Additional name",
    "Family name",
    "Suffix",
    "Telephone",
    "Home phone",
    "Cell phone",
    "Mobile phone",
    "Work phone",
    "Preferred phone",
    "Email",
    "Address",
    "Note",
    "Birthday",
]


class PhoneNumbers:
    fields = ("cell", "home", "mobile", "phone", "preferred", "work")
    __slots__ = fields

    def __init__(
        self, cell=None, home=None, mobile=None, phone=None, preferred=None, work=None
    ):
        self.cell = cell
        self.home = home
        self.mobile = mobile
        self.phone = phone
        self.preferred = preferred
        self.work = work

    def __repr__(self):
        args_repr = [
            "{}={}".format(attr, repr(getattr(self, attr))) for attr in self.fields
        ]
        self_repr = self.__class__.__name__ + "({})".format(", ".join(args_repr))
        return self_repr

    def __str__(self):
        args_str = [
            "{}={}".format(attr, repr(getattr(self, attr))) for attr in self.fields
        ]
        self_str = self.__class__.__name__ + "({})".format(", ".join(args_str))
        return self_str


def get_phone_numbers(vCard):
    phone_numbers = PhoneNumbers()
    for tel in vCard.tel_list:
        if vCard.version.value == "2.1":
            # tel.value should already be a string.
            tel_value = tel.value.strip()
            params = [param.lower() for param in tel.singletonparams]
            if params == []:
                phone_numbers.phone = tel_value
            elif "cell" in params:
                phone_numbers.cell = tel_value
            elif "work" in params:
                phone_numbers.work = tel_value
            elif "home" in params:
                phone_numbers.home = tel_value
            elif "mobile" in params:
                phone_numbers.mobile = tel_value
            elif "pref" in params:
                phone_numbers.preferred = tel_value
            else:
                logger.warning(
                    "Warning: Unrecognized phone number category in %s",
                    repr(vCard.tel_list),
                )
                logger.info("tel = %s", tel.prettyPrint())
        elif vCard.version.value == "3.0":
            # tel.value should already be a string.
            tel_value = tel.value.strip()
            if "TYPE" in tel.params:
                telephone_type = [val.lower() for val in tel.params["TYPE"]]
                if "cell" in telephone_type:
                    phone_numbers.cell = tel_value
                elif "work" in telephone_type:
                    phone_numbers.work = tel_value
                elif "home" in telephone_type:
                    phone_numbers.home = tel_value
                elif "mobile" in telephone_type:
                    phone_numbers.mobile = tel_value
                elif "pref" in telephone_type:
                    phone_numbers.preferred = tel_value
                else:
                    logger.warning(
                        "Unrecognized phone number category in %s", repr(vCard.tel_list)
                    )
                    tel.prettyPrint()
            else:
                phone_numbers.phone = tel_value
        else:
            raise NotImplementedError(
                "Version not implemented: {}".format(vCard.version.value)
            )

    logger.debug("phone_numbers = %s", phone_numbers)
    return phone_numbers


def get_info_list(vCard, vcard_filepath):
    vcard = collections.OrderedDict()
    for column in column_order:
        vcard[column] = None
    name = cell = work = home = mobile = None
    vCard.validate()
    for key, val in list(vCard.contents.items()):
        if key == "fn":
            logger.debug("fn = %s", repr(vCard.fn.value))
            vcard["Formatted Name"] = vCard.fn.value
        elif key == "n":
            logger.debug("n = %s", repr(vCard.n.value))
            vcard["Name"] = str(vCard.n.value).strip()
            vcard["Prefix"] = vCard.n.value.prefix
            vcard["Given name"] = vCard.n.value.given
            vcard["Additional name"] = vCard.n.value.additional
            vcard["Family name"] = vCard.n.value.family
            vcard["Suffix"] = vCard.n.value.suffix
        elif key == "tel":
            logger.debug("tel_list = %s", repr(vCard.tel_list))
            phone_numbers = get_phone_numbers(vCard)
            vcard["Telephone"] = phone_numbers.phone
            vcard["Cell phone"] = phone_numbers.cell
            vcard["Home phone"] = phone_numbers.home
            vcard["Work phone"] = phone_numbers.work
            vcard["Mobile phone"] = phone_numbers.mobile
            vcard["Preferred phone"] = phone_numbers.preferred
        elif key == "email":
            logger.debug("email = %s", repr(vCard.email.value))
            email = str(vCard.email.value).strip()
            vcard["Email"] = email
        elif key == "note":
            logger.debug("note = %s", repr(vCard.note.value))
            note = str(vCard.note.value)
            vcard["Note"] = note
        elif key == "adr":
            logger.debug("adr = %s", repr(vCard.adr.value))
            adr = str(vCard.adr.value).strip()
            if adr.startswith('"') and adr.endswith('"'):
                adr = adr[1:-1]
            vcard["Address"] = adr
        elif key == "bday":
            bday = str(vCard.bday.value).strip()
            vcard["Birthday"] = bday
        elif key == "version":
            # Ignore the key for vcard version
            pass
        else:
            logging.warning(
                "unused key {} in file {}".format(repr(key), repr(vcard_filepath))
            )
            # An unused key, like `adr`, `title`, `url`, etc.
            pass
    if name is None:
        logger.warning("no name for vCard in file %s", repr(vcard_filepath))
    if all(telephone_number is None for telephone_number in [cell, work, home, mobile]):
        logger.warning(
            "no telephone numbers for file %s with name %s",
            repr(vcard_filepath),
            repr(name),
        )

    return vcard


def get_vcards(vcard_filepath):
    with open(vcard_filepath) as fp:
        all_text = fp.read()
    for vCard in vobject.readComponents(all_text):
        yield vCard


def readable_directory(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError("not an existing directory: {}".format(path))
    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError("not a readable directory: {}".format(path))
    return path


def writable_file(path):
    if os.path.exists(path):
        if not os.access(path, os.W_OK):
            raise argparse.ArgumentTypeError("not a writable file: {}".format(path))
    else:
        # If the file doesn't already exist,
        # the most direct way to tell if it's writable
        # is to try writing to it.
        with open(path, "w") as fp:
            pass
    return path


def main():
    parser = argparse.ArgumentParser(
        description="Convert a bunch of vCard (.vcf) files to a single TSV file."
    )
    parser.add_argument(
        "read_dir", type=readable_directory, help="Directory to read vCard files from."
    )
    parser.add_argument(
        "tsv_file",
        type=writable_file,
        help="Output file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="More verbose logging",
        dest="loglevel",
        default=logging.WARNING,
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Enable debugging logs",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    parser.add_argument(
        "-r",
        "--recursive",
        help="Recursively search for vcard files in the specified directory & subdirectories",
        action="store_true",
        dest="is_recursive",
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    logger.setLevel(args.loglevel)

    if args.is_recursive:
        vcard_pattern = os.path.join(args.read_dir, "**/*.vcf")
    else:
        vcard_pattern = os.path.join(args.read_dir, "*.vcf")
    vcard_paths = sorted(glob.glob(vcard_pattern, recursive=args.is_recursive))
    if len(vcard_paths) == 0:
        logger.error("no files ending with `.vcf` in directory %s", repr(args.read_dir))
        raise FileNotFoundError

    # Tab separated values are less annoying than comma-separated values.
    with open(args.tsv_file, "w", encoding="utf-8", newline="") as tsv_fp:
        writer = csv.writer(tsv_fp, delimiter="\t")
        writer.writerow(column_order)

        for vcard_path in vcard_paths:
            logging.info("vcard_path = {}".format(repr(vcard_path)))
            for vcard in get_vcards(vcard_path):
                vcard_info = get_info_list(vcard, vcard_path)
                writer.writerow(list(vcard_info.values()))


if __name__ == "__main__":
    main()
