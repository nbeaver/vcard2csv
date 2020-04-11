.. -*- coding: utf-8 -*-

============
vCard to CSV
============

:author: Nathaniel Beaver

This is a Python 2/3 script to turn a directory full of vCard files
into a single CSV file.
It can also be imported and used as a module.

Not all of the vCard fields are preserved; currently only these fields:

- Name
- Cell phone
- Work phone
- Home phone
- Email
- Note

(I used this to convert vCards from an old LG Rumor 2 cell phone,
so I have not needed to extract additional fields.)

------------
Dependencies
------------

If you encounter an error like this (Python 2)::

    Traceback (most recent call last):
      File "vcard2csv.py", line 2, in <module>
        import vobject # to parse vCard (vcf) files
    ImportError: No module named vobject

or this (Python 3)::

    Traceback (most recent call last):
      File "vcard2csv.py", line 2, in <module>
        import vobject
    ModuleNotFoundError: No module named 'vobject'


then you need to install the python `vobject`_ library,
which you can do with pip::

    pip install --user vobject

.. _vobject: http://vobject.skyhouseconsulting.com/

It is also in the major package managers.

https://src.fedoraproject.org/rpms/python-vobject

https://launchpad.net/ubuntu/+source/python-vobject

https://tracker.debian.org/pkg/python-vobject

https://security.archlinux.org/package/python-vobject

https://software.opensuse.org/package/python-vobject

https://software.opensuse.org/package/python2-vobject

https://software.opensuse.org/package/python3-vobject

-----
Usage
-----

The vCard files must have the suffix ``.vcf``.
Simply run the script in the directory containing the vCard files
and specify the output filename::

    python vcard2csv.py . foo.csv

Or point the script at a directory containing the ``.vcf`` files::

    python vcard2csv.py example-vcards foo.csv

For additional help and options, pass the ``-h`` flag::

    python vcard2csv.py -h

The script is compatible with both Python 2 and Python 3.

----
Bugs
----

Only a few of the vCard fields are preserved;
this may be undesirable.

vCard version 4.0 has not been implemented,
though it would probably be straightforward to do so.

See the `to-do list`_ for more.

.. _to-do list: todo.md

-------
License
-------

This project is licensed under the terms of the `MIT license`_.

.. _MIT license: LICENSE.txt
