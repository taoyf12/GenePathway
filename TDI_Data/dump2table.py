# Extract data from dump file.


PATH = '../TDI_dump/tbd.sql'

# sga_id to gen_id
sgaid2genid = {}
PATH = '../TDI_dump/SGAs.sql'
i = 0
for line in open(PATH, 'r'):
    i += 1
    values = line.split('),(')
    if 'INSERT INTO' in values[0]:
    	# modify first and last string in list.
        values[-1] = values[-1][:-3]
        tmp = values[0].split('(')
        values[0] = tmp[1]
        # val: 45009,181,3437,NULL,'TCGA-13-0751','CDH11'
        for val in values:
        	row = val.split(',')
        	#print row[0], row[2]
        	# TODO: row[2] can be NULL...?
        	sgaid2genid[row[0]] = row[2]

print len(sgaid2genid)
for i in range(1,10):
    print sgaid2genid['{}'.format(i)]

