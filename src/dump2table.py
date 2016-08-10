
from collections import defaultdict as dd
import io
from random import shuffle

def readTDI(path, pos_sga, pos_deg):
    '''
    Aggregate all the (sgaid, degid) pairs.
    path: dir of .sql file.
    pos_sga: position of sgaid.
    pos_deg: position of degid.
    '''
    print 'reading from: {}...'.format(path)
    sga2deg = set()
    for line in open(path, 'r'):
        values = line.split('),(')
        if 'INSERT INTO' in values[0]:
            values[-1] = values[-1][:-3]
            tmp = values[0].split('(')
            values[0] = tmp[1]
            for val in values:
                row = val.split(',')
                if row[pos_sga] != 'NULL':
                    sga2deg.add((row[pos_sga],row[pos_deg]))
    #sga2deg = list(sga2deg)
    #sga2deg = sorted(sga2deg, key = lambda item:(int(item[0]),int(item[1])))
    print 'len(sgaid2degid) = {}'.format(len(sga2deg))
    return sga2deg

def readSQL(path, pos_src, pos_dist):
    '''
    Read LUT from .sql file.
    src2dist: a dictionary
    '''
    print 'reading from: {}...'.format(path)
    src2dist = {}
    for line in open(path, 'r'):
        values = line.split('),(')
        if 'INSERT INTO' in values[0]:
            # modify first and last string in list.
            values[-1] = values[-1][:-3]
            tmp = values[0].split('(')
            values[0] = tmp[1]
            for val in values:
                row = val.split(',')
                src2dist[row[pos_src]] = row[pos_dist]

    print 'len = {}'.format(len(src2dist))
    return src2dist

def save2txt(path, table):
    '''
    path: the filename to be saved.
    table: list of string list, data to be saved.
    '''
    print 'saving to {}...'.format(path)
    f = open(path, 'w')
    for row in table:
        print >> f, '\t'.join(row)
    f.close()

if __name__ == '__main__':

    # Extract (sga, deg) pairs from dumped .sql file.
    path_tdi = '../TDI_dump/TDI_Results.sql'
    sgaid2degid = readTDI(path_tdi,2,4)

    path_sga = '../TDI_dump/SGAs.sql'
    sgaid2genid = readSQL(path_sga,0,2)

    path_deg = '../TDI_dump/DEGs.sql'
    degid2genid = readSQL(path_deg,0,2)

    path_gen = '../TDI_dump/Genes.sql'
    genid2gen = readSQL(path_gen,0,1)

    sga2deg = set()
    for row in sgaid2degid:
        sgaid_tmp = sgaid2genid[row[0]]
        degid_tmp = degid2genid[row[1]]
        # sga is unit, no corresponding genid.
        if sgaid_tmp == 'NULL':
            continue
        else:
            sga = genid2gen[sgaid_tmp]
            deg = genid2gen[degid_tmp]
            # normalize to lower case gene representation.
            sga2deg.add((sga[1:-1].lower(),deg[1:-1].lower()))
    sga2deg = list(sga2deg)
    sga2deg = sorted(sga2deg, key = lambda item:(item[0], item[1]))

    # prepare the files required by ProPPR.



    path_sga2deg = '../TDI_dump/sga2deg.txt'
    save2txt(path_sga2deg, sga2deg)