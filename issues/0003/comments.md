Hi @LatinSuD, thanks for your interest in this script. I believe this is essentially the same issues as https://github.com/nbeaver/vcard2csv/issues/2 although in your case you've provided an anonymized example which is quite helpful.

One thing that makes this a bit tricky is that the type parameter could be just about anything, so the columns of the generated TSV could vary greatly depending on the input files. I'll need to think a bit to decide the best way to go about this in a consistent way, since I intended this script to be used on a particular set of vCards with consistent field values, not on arbitrary heterogeneous collections of vCard files. You may find it more expedient to just adapt the script to your particular collection of vCards rather than waiting for me to write a solution that properly handles the general case.

---
