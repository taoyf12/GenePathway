# Extract data from dump file.

# sga_id to gen_id

def readSQL(path, pos_src, pos_dist):
    print 'reading from: {}...'.format(path)
    src2dist = {}
    i = 0
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
                src2dist[row[pos_src]] = row[pos_dist]

    print len(src2dist)
    for i in range(1,10):
        print src2dist['{}'.format(i)]
    return src2dist

if __name__ == '__main__':
    path_sga = '../TDI_dump/SGAs.sql'
    #sgaid2genid = {}
    sgaid2genid = readSQL(path_sga,0,2)
    path_deg = '../TDI_dump/DEGs.sql'
    degid2genid = readSQL(path_deg,0,2)
    path_gen = '../TDI_dump/Genes.sql'
    genid2gen = readSQL(path_gen,0,1)
    # print sgaid2genid

