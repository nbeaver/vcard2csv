# coding: utf-8
import vobject
import glob
for file in glob.glob("*.vcf"):
    print file
    s = open(file).read()
    v = vobject.readOne(s)
    print v.prettyPrint()
