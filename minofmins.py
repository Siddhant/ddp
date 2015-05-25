mfile = open('minimums', 'r')

mins = []

for line in mfile:
    a, b, v = line.split()
    mins.append(float(v))
    
print min(mins)
