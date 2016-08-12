# Prepare date from raw data.
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
    table: list of string list / set of tuples, data to be saved.
    '''
    print 'saving to {}...'.format(path)
    f = open(path, 'w')
    for row in table:
        print >> f, '\t'.join(row)
    f.close()

def save2txt_list(path, table):
    '''
    path: the filename to be saved.
    table: list/set of string, data to be saved.
    '''
    print 'saving to {}...'.format(path)
    f = open(path, 'w')
    for row in table:
        print >> f, row
    f.close()

def buildPathway(path):
    '''
    Based on pathway.cfacts raw data, remove nodes not connected
    to others.
    Build graph corpus.
    
    '''
    print 'reading from: {}...'.format(path)
    corpus = set()
    pathway = set()
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        genex = values[1].lower()
        geney = values[2].lower()
        # TODO:
        # we don't include the loop edge to itself
        if (genex != geney):
            corpus.add(genex)
            corpus.add(geney)
            pathway.add(('leadTo',genex,geney,'1.0000'))
    print 'len(pathway) = {}'.format(len(pathway))
    print 'len(node) = {}'.format(len(corpus))
    return corpus, pathway

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
            sga = sga[1:-1].lower()
            deg = deg[1:-1].lower()
            # TODO:
            # sga and deg should be different.
            if sga != deg:
                sga2deg.add((sga,deg))

    # prepare the files required by ProPPR.
    path_pathway = '../TDI_dump/pathway.cfacts'
    corpus, pathway = buildPathway(path_pathway)
    path_pathway_out = '../pathway/pathway.graph'
    save2txt(path_pathway_out, pathway)

    # (sga,deg) pairs within the pathway.graph
    sga2deg_out = set()
    deg_corpus = set()
    for values in sga2deg:
        genex = values[0]
        geney = values[1]
        if (genex in corpus) and (geney in corpus):
            # genex and geney won't be same, we have examined it before.
            sga2deg_out.add((genex,geney))
            deg_corpus.add(geney)
    # sga2deg_out = sorted(sga2deg_out, key = lambda item:(item[0],item[1]))
    sga2deg = sga2deg_out
    print 'len(sga2deg) = {}'.format(len(sga2deg))

    path_label = '../pathway/labels.cfacts'
    print 'saving to {}...'.format(path_label)
    f = open(path_label,'w')
    for gene in deg_corpus:
        print >> f, 'isDEG\t'+gene
    f.close
    # TODO: Problem here.
    print 'len(deg) = {}'.format(len(deg_corpus))

    sga2deg_list = dd(list)
    for line in sga2deg:
        sga = line[0]
        deg = line[1]
        sga2deg_list[sga].append(deg)

    path_all = '../pathway/examples'
    print 'saving to {}...'.format(path_all)
    with io.open(path_all,'w') as file:
        for _, sga in enumerate(sga2deg_list):
            deg = sga2deg_list[sga]
            file.write(u'pathTo(%s,Y)'%sga)
            # TODO:
            for gene in deg_corpus:
                # TODO:
                if gene in deg:
                    file.write(u'\t+')
                else:
                    file.write(u'\t-')
                file.write(u'pathTo(%s,%s)'%(sga,gene))
            file.write(u'\n')

    examples = []
    for line in open(path_all, 'r'):
        line = line.strip()
        examples.append(line)

    print 'len(samples) = {}'.format(len(examples))
    shuffle(examples)
    thresh1 = 0.1
    thresh2 = 0.2
    cut1 = int(thresh1*len(examples))
    cut2 = int(thresh2*len(examples))
    train = examples[0:cut1]
    test = examples[cut1:cut2]
    remain = examples[cut2:len(examples)]

    path_train = '../pathway/train.examples'
    path_test = '../pathway/test.examples'
    path_remain = '../pathway/remain.examples'
    save2txt_list(path_train,train)
    save2txt_list(path_test,test)
    save2txt_list(path_remain,remain)
    # print 'saving to {}...'.format(path_train)
    # f = open(path_train,'w')
    # for line in train:
    #     print >> f, line
    # f.close

    # print 'saving to {}...'.format(path_test)
    # f = open(path_test,'w')
    # for line in test:
    #     print >> f, line
    # f.close

    print 'Done!'


