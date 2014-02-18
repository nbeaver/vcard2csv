#!/usr/bin/env python
import vobject
import glob
for file in glob.glob("*.vcf"):
    print file
    s = open(file).read()
    v = vobject.readOne(s)
    try print v.tel.value
    try print v.tel.value
    try print v.email.value
    try print v.note.value
else:
    import code
    code.interact(local=locals())
