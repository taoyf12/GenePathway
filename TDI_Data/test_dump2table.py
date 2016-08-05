# Extract data from dump file.

def readSQL(path, pos_tdi, pos_pat, pos_src, pos_dist, pos_pro = -1):
    print 'reading from: {}...'.format(path)
    src2dist = {}
    i = 0

    f = open('out.txt', 'w')

    for line in open(path, 'r'):
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
                # TODO: row[2] can be NULL...?
                # print '{} \t {} \t {} \t {} \n}'.format(row[pos_pat],row[pos_src],row[pos_dist],row[pos_pro])
                print >> f, '{}\t{}\t{}\t{}\t{}'.format(row[pos_tdi], row[pos_pat],row[pos_src],row[pos_dist],row[pos_pro])
                #print '{}'.format(row[pos_pat])
                #sys.stdout = orig_stdout
                

                # src2dist[(row[pos_src],row[pos_dist])] = row[pos_pro]
    f.close()
    print len(src2dist)
    # for i in range(1,10):
    #     print src2dist['{}'.format(i)]
    return src2dist

if __name__ == '__main__':
    # sga_id to gen_id
    path_tdi = '../TDI_dump/TDI_Results.sql'
    lookuptable = readSQL(path_tdi,0,1,2,4,5)


