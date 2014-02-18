#!/usr/bin/env python
import vobject
import glob
for file in glob.glob("*.vcf"):
    print file
    s = open(file).read()
    v = vobject.readOne(s)
    print v.tel.value
    print v.tel.value
    print v.email.value
    print v.note.value
else:
    import code
    code.interact(local=locals())
