import sys
import re

dfile = open(sys.argv[1], "r")
pfile = open(re.sub(".def", ".points", sys.argv[1]), "w")

for line in dfile:
    if line.startswith('COMPONENTS'):
        no_components = line.split()[1]
        break
print "number of components =", no_components

for line in dfile:
    if line.startswith('- U'):
        pfile.write(' '.join(i for i in line.split()[6:8]))
        pfile.write('\n')
    else:
        if line.startswith('END COMPONENTS'):
            break     
