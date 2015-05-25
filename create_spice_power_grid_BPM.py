import sys
import re
import collections
import itertools    # for Cartesian product

# open the .points file
pfile = open(sys.argv[1], "r")

x_coords = []
y_coords = []

for line in pfile:
    x, y = line.split()
    x_coords.append(x)
    y_coords.append(y)
    
x_uniq_count = collections.Counter(x_coords)
y_uniq_count = collections.Counter(y_coords)

x_uniq_sorted = sorted(int(_) for _ in x_uniq_count)
#print x_uniq_sorted
y_uniq_sorted = sorted(int(_) for _ in y_uniq_count)
#print y_uniq_sorted

total_no_of_nodes = len(x_uniq_sorted)*len(y_uniq_sorted)
#print total_no_of_nodes

# calculate distance between adjacent points, first vertically then horizontally
vertical_lengths = []
for i in xrange(len(y_uniq_sorted)-1):
    vertical_lengths.append(y_uniq_sorted[i+1]-y_uniq_sorted[i])
# print vertical_lengths
    
horizontal_lengths = []
for i in xrange(len(x_uniq_sorted)-1):
    horizontal_lengths.append(x_uniq_sorted[i+1]-x_uniq_sorted[i])
# print horizontal_lengths


# now we are ready to create the netlist:

# create a SPICE netlist for power grid
cfile = open(re.sub(".points", "_power_grid_BPM_with_currents.cir", sys.argv[1]), "w")

cfile.write(".title 1-layer Power Grid for" + " " + sys.argv[1] + "\n")

cfile.write("""\
* resistance segment model:
.subckt Rseg 1 3
R1 1 2 0.583
L1 2 3 0.003n
C1 1 0 0.25e-12
C2 3 0 0.25e-12
.ends
""")

count_R = 0

# assuming copper wires, and some process i looked up somewhere:
# the resistnace (in ohm) per unit leght (in metre) was calculated as:
R_per_metre = 11492
# hence the resistance per micrometer:
R_per_micron = float(11492)/10e6
# but, the def files use a unit of length such that 2000 units = 1 micron
R_per_unit = R_per_micron/2000
#print R_per_unit

# do a Cartesian product of x and y coordinates to get coordinates of all nodes
all_nodes = list(itertools.product(x_uniq_sorted, y_uniq_sorted))
#print all_nodes

#first the horizontal resistors:
cfile.write("* the horizontal resistors:" + "\n")

# we shall create two lists, l and r, to track the left and right nodes respectively

l = []
r = []

# create l
k = 0
for y in y_uniq_sorted:
    for x in x_uniq_sorted:
        k = k + 1
        if k % len(x_uniq_sorted) == 0 :
            continue
        else:
            l.append((x, y))
            
#print l
            
# create r
k = 0
for y in y_uniq_sorted:
    for x in x_uniq_sorted:
        k = k + 1
        if k % len(x_uniq_sorted) == 1:
            continue
        else:
            r.append((x, y))
            
#print r

# now we can start creating the resistors:
for p in itertools.izip(l, r, itertools.cycle(horizontal_lengths)):
    le = p[0] # le(ft)
    ri = p[1] # ri(ght)
    length = p[2]
    
    count_R = count_R + 1
    
    cfile.write("X" + str(count_R) + " ")
    # lower node:
    cfile.write("n_" + str(le[0]) + "_" + str(le[1]) + " ")
    # upper node:
    cfile.write("n_" + str(ri[0]) + "_" + str(ri[1]) + " ")
    # resistance value:
    cfile.write("Rseg")
        
    cfile.write("\n")

        
# now the vertical resistors:
cfile.write("* the vertical resistors:" + "\n")

# we shall create two lists, l and u, to track lower and upper nodes respetively

l = []
u = []

# create l
k = 0
for x in x_uniq_sorted:
    for y in y_uniq_sorted:
        k = k + 1
        if k % len(y_uniq_sorted) == 0 :
            continue
        else:
            l.append((x, y))
    
# create u
k = 0
for x in x_uniq_sorted:
    for y in y_uniq_sorted:
        k = k + 1
        if k % len(y_uniq_sorted) == 1 :
            continue
        else:
            u.append((x, y))

# now we can start creating the resistors:
for p in itertools.izip(l, u, itertools.cycle(vertical_lengths)):
    lo = p[0] # lo(wer)
    up = p[1] # up(per)
    length = p[2]
    count_R = count_R + 1
    
    cfile.write("X" + str(count_R) + " ")
    # lower node:
    cfile.write("n_" + str(lo[0]) + "_" + str(lo[1]) + " ")
    # upper node:
    cfile.write("n_" + str(up[0]) + "_" + str(up[1]) + " ")
    # resistance value:
    cfile.write("Rseg")
        
    cfile.write("\n")
    
cfile.write('* voltage source is placed at (x_min, y_min)' + "\n")
cfile.write('Vin' + ' ' + 'n_' + str(x_uniq_sorted[0]) + '_' + str(y_uniq_sorted[0]) + ' 0 DC 1.0' + "\n")
cfile.write("\n")

# now add the currents (source copied from translate2i.py):
sfile = open(sys.argv[2], 'r')

no_primary_inputs = int(sys.argv[3])

count_I = 0

#offset keeps track of which cyccle we are in
cycle_number = -1
cycle_period = 2000 # in picoseconds

def calc_offset():
    return cycle_number*cycle_period

for line in sfile:
    line = line.strip()
    items = line.split(',')
    if len(items) == 6:
        # skip the next lines (#PI-1) because they are not toggle information:
        for i in xrange(no_primary_inputs-1):
            sfile.next()
        # next line we will read is gonna be gate toggle information,
        # therefore, we are in the next cycle
        cycle_number = cycle_number+1
        # calculate new offset:
        offset = calc_offset()
    if len(items) == 8:
        if items[3] == '1':
            x = items[-2]
            y = items[-1]
            count_I = count_I + 1
            cfile.write('I'+ str(count_I) + ' n_' + str(x) + '_' + str(y)+ ' ' + '0' + ' ')
            cfile.write('PWL(' + str(offset) + 'ps 0uA ' + str(offset+30) + 'ps 0uA ' + str(offset+31) + 'ps 30uA ' + str(offset+59) + 'ps 30uA ' + str(offset+60) + 'ps 0uA)')
            cfile.write("\n")
    else:
        print "malformed toggle file"

# we do transient simulation for how long?
# we use the last value of offset, but to be on the safe side, do for 2 more cycles
cfile.write(".tran 1ps " + str(offset+2*cycle_period) + "ps")
cfile.write("""
.control
run
""")

# calculate minimum value of each voltage vector
cfile.write('* calculate minimum value of voltage at each node:\n')
for x in x_uniq_sorted:
    for y in y_uniq_sorted:
        cfile.write('let min_' + str(x) + '_' + str(y) + " = minimum(v(n_" + str(x) + '_' + str(y) + "))\n")

# write(append) the minumum values found above to a file called 'minimums'
cfile.write('* now write(append) all minimums to a file. ">>" means append:\n')
for x in x_uniq_sorted:
    for y in y_uniq_sorted:
        cfile.write('print min_' + str(x) + '_' + str(y) + " >> minimums\n")
        
# just dump all the voltage vectors:       
#for x in x_uniq_sorted:
#    for y in y_uniq_sorted:
#        cfile.write('wrdata v(n_' + str(x) + '_' + str(y) + ') v(n_' + str(x) + '_' + str(y) + ")\n")
                
       
cfile.write("\nexit\n.endc")


