import sys

sfile = open(sys.argv[1], 'r')
ifile = open('currents' , 'w')

no_primary_inputs = int(sys.argv[2])

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
    else:
        if items[3] == '1':
            x = items[-2]
            y = items[-1]
            count_I = count_I + 1
            ifile.write('I'+ str(count_I) + ' n_' + str(x) + '_' + str(y)+ ' ' + '0' + ' ')
            ifile.write('PWL(' + str(offset) + 'ps 0uA ' + str(offset+30) + 'ps 0uA ' + str(offset+31) + 'ps 30uA ' + str(offset+59) + 'ps 30uA ' + str(offset+60) + 'ps 0uA)')
#           ifile.write('PULSE(0uA 30uA 30ps 0 0 30ps 2n)')
            ifile.write("\n")
            
print "last offest used =", offset
            
