#!/usr/bin/env python
import vobject
import glob
for file in glob.glob("*.vcf"):
    print file
    s = open(file).read()
    v = vobject.readOne(s)
    try:
        print v.n.value
    except AttributeError:
        print "Could not find name"
	pass
    try:
        print v.tel.value
    except AttributeError:
        print "Could not find telephone number"
	pass
    try:
        print v.email.value
    except AttributeError:
        pass
    try:
        print v.note.value
    except AttributeError:
        pass
else: # Last for loop iteration
    import code
    code.interact(local=locals())
