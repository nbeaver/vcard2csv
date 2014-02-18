#!/usr/bin/env python
import vobject
import glob
for file in glob.glob("*.vcf"):
    print file
    vCard_text = open(file).read()
    vCard = vobject.readOne(vCard_text)
    try:
        print vCard.n.value
    except AttributeError:
        print "Could not find name"
	pass
    try:
        print vCard.tel.value
    except AttributeError:
        print "Could not find telephone number"
	pass
    try:
        print vCard.email.value
    except AttributeError:
        pass
    try:
        print vCard.note.value
    except AttributeError:
        pass
else: # Last for loop iteration
    import code
    code.interact(local=locals())
