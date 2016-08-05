# Extract data from dump file.
# sort -k 2g -k 3g -k 4g out.txt > test2.txt

path = 'test2.txt'
print 'reading from: {}...'.format(path)
i = 0
f = open('test3.txt', 'w')

values_pro = ['','','','','']
for line in open(path, 'r'):
    i += 1
    values = line.split('\t')
    values[-1] = values[-1][:-1]
    if (values_pro[1] == values[1]) and (values_pro[2] == values[2]) and (values_pro[3] == values[3]):
        #print 'same{}'.format(i)
        values_pro = values
        continue
        # if values_pro[4] != values[4]:
        #     print 'same{}'.format(i)
        #     print 'wrong!!!!!!!!!!!!!!!!!!!!!!!!!!'
    elif values[2] == 'NULL':
        values_pro = values
        continue
    else:
        values_pro = values
        print >> f, '{}\t{}\t{}\t{}'.format(values[1],values[2],values[3],values[4])
    #print values
        # # modify first and last string in list.
        # values[-1] = values[-1][:-3]
        # tmp = values[0].split('(')
        # values[0] = tmp[1]
        # # val: 11769453        1       303     4147    0.35546
        # # tdi_id, patient_id, SGA_id, DEG_id, posterior
        # for val in values:
        #     row = val.split(',')
        #     # TODO: row[2] can be NULL...?
        #     print >> f, '{}\t{}\t{}\t{}\t{}'.format(row[pos_tdi], row[pos_pat],row[pos_src],row[pos_dist],row[pos_pro])

f.close()


