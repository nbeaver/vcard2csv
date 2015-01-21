.. -*- coding: utf-8 -*-

============
vCard to CSV
============

:Author: Nathaniel Beaver

This is a script to turn a directory full of vCard files into a single CSV file.
Not all of the vCard fields are preserved; only name, phone numbers, email, and notes.

It can also be imported and used as a module.

------------
Dependencies
------------

If you encounter an error like this::

    Traceback (most recent call last):
      File "vcard-to-csv.py", line 2, in <module>
        import vobject # to parse vCard (vcf) files
    ImportError: No module named vobject

then you need to install the python `vobject`_ library,
which you can do with pip::

    pip install vobject

It is also in the major package managers.

.. _vobject: http://vobject.skyhouseconsulting.com/

https://admin.fedoraproject.org/pkgdb/package/python-vobject/

http://packages.ubuntu.com/search?keywords=python-vobject

https://tracker.debian.org/pkg/python-vobject

https://aur.archlinux.org/packages/python2-vobject/

-----
Usage
-----

The vCard files must have the suffix ``.vcf``.
Simply run the script in the directory containing the vCard files and specify the output filename::

    python vcard-to-csv.py foo.csv

----
Bugs
----

Only a few of the vCard fields are preserved;
this may be undesirable.

vCard version 4.0 has not been implemented,
though it would probably be straightforward to do so.
