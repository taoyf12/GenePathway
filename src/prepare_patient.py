# Prepare date from raw data.
from collections import defaultdict as dd
import io
import random

def readTDI_tuple(path, pos_patient, pos_sga, pos_deg):
    '''
    Collect all the (patient_id, sgaid, degid) tuples.
    path: dir of .sql file.
    pos_sga: position of sgaid.
    pos_deg: position of degid.
    '''
    print 'reading from: {}...'.format(path)
    sga2deg = []
    for line in open(path, 'r'):
        values = line.split('),(')
        if 'INSERT INTO' in values[0]:
            values[-1] = values[-1][:-3]
            tmp = values[0].split('(')
            values[0] = tmp[1]
            for val in values:
                row = val.split(',')
                if row[pos_sga] != 'NULL':
                    sga2deg.append((int(row[pos_patient]),row[pos_sga],row[pos_deg]))
    #sga2deg = list(sga2deg)
    #sga2deg = sorted(sga2deg, key = lambda item:(int(item[0]),int(item[1])))
    print 'len(patid2sgaid2degid) = {}'.format(len(sga2deg))
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
            # TODO: 1.0000
            # median
            pathway.add(('leadTo',genex,geney,'1.0000'))
    print 'len(pathway) = {}'.format(len(pathway))
    print 'len(node) = {}'.format(len(corpus))
    return corpus, pathway

if __name__ == '__main__':

    # Extract (sga, deg) pairs from dumped .sql file.



    # print patid_train,len(patid_train)

    # print patid,len(patid)

    path_tdi = '../TDI_dump/TDI_Results.sql'
    patid2sgaid2degid = readTDI_tuple(path_tdi,1,2,4)

    path_sga = '../TDI_dump/SGAs.sql'
    sgaid2genid = readSQL(path_sga,0,2)

    path_deg = '../TDI_dump/DEGs.sql'
    degid2genid = readSQL(path_deg,0,2)

    path_gen = '../TDI_dump/Genes.sql'
    genid2gen = readSQL(path_gen,0,1)


    # Randomly generate train, test and remain set.
    NUM_PAT = 4468
    patid = range(1,NUM_PAT+1)
    SEED = 888
    random.seed(SEED)
    random.shuffle(patid)

    thresh1 = 0.1
    thresh2 = 0.2
    cut1 = int(thresh1*NUM_PAT)
    cut2 = int(thresh2*NUM_PAT)
    patid_train = patid[0:cut1]
    patid_test = patid[cut1:cut2]
    patid_remain = patid[cut2:NUM_PAT]


    sga2deg_train = set()
    sga2deg_test = set()
    sga2deg_remain = set()
    sga2deg = set()
    for row in patid2sgaid2degid:
        patid = row[0]
        sgaid_tmp = sgaid2genid[row[1]]
        degid_tmp = degid2genid[row[2]]
        #print patid
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
                if patid in patid_train:
                    sga2deg_train.add((sga,deg))
                elif patid in patid_test:
                    sga2deg_test.add((sga,deg))
                elif patid in patid_remain:
                    sga2deg_remain.add((sga,deg))

                    
    # prepare the files required by ProPPR.
    path_pathway = '../TDI_dump/pathway.cfacts'
    corpus, pathway = buildPathway(path_pathway)
    path_pathway_out = '/usr1/public/yifeng/pathway_patient/pathway.graph'
    save2txt(path_pathway_out, pathway)


    # (sga,deg) pairs within the pathway.graph
    sga2deg_out_train = set()
    sga2deg_out_test = set()
    sga2deg_out_remain = set()    
    deg_corpus = set()
    for values in sga2deg_train:
        genex = values[0]
        geney = values[1]
        if (genex in corpus) and (geney in corpus):
            # genex and geney won't be same, we have examined it before.
            sga2deg_out_train.add((genex,geney))
            deg_corpus.add(geney)
    for values in sga2deg_test:
        genex = values[0]
        geney = values[1]
        if (genex in corpus) and (geney in corpus):
            # genex and geney won't be same, we have examined it before.
            sga2deg_out_test.add((genex,geney))
            deg_corpus.add(geney)
    for values in sga2deg_remain:
        genex = values[0]
        geney = values[1]
        if (genex in corpus) and (geney in corpus):
            # genex and geney won't be same, we have examined it before.
            sga2deg_out_remain.add((genex,geney))
            deg_corpus.add(geney)

    # sga2deg_out = sorted(sga2deg_out, key = lambda item:(item[0],item[1]))
    sga2deg_train = sga2deg_out_train
    sga2deg_test = sga2deg_out_test
    sga2deg_remain = sga2deg_out_remain
    print 'len(sga2deg_train) = {}'.format(len(sga2deg_train))
    print 'len(sga2deg_test) = {}'.format(len(sga2deg_test))
    print 'len(sga2deg_remain) = {}'.format(len(sga2deg_remain))

    path_label = '/usr1/public/yifeng/pathway_patient/labels.cfacts'
    print 'saving to {}...'.format(path_label)
    f = open(path_label,'w')
    for gene in deg_corpus:
        print >> f, 'isDEG\t'+gene
    f.close
    # TODO: Problem here.
    print 'len(deg) = {}'.format(len(deg_corpus))

    sga2deg_list_train = dd(list)
    sga2deg_list_test = dd(list)
    sga2deg_list_remain = dd(list)
    for line in sga2deg_train:
        sga = line[0]
        deg = line[1]
        sga2deg_list_train[sga].append(deg)
    for line in sga2deg_test:
        sga = line[0]
        deg = line[1]
        sga2deg_list_test[sga].append(deg)
    for line in sga2deg_remain:
        sga = line[0]
        deg = line[1]
        sga2deg_list_remain[sga].append(deg)



    path_sga2deg = '/usr1/public/yifeng/pathway_patient/sga2deg_train.examples'
    save2txt(path_sga2deg,sga2deg_train)
    path_sga2deg = '/usr1/public/yifeng/pathway_patient/sga2deg_test.examples'
    save2txt(path_sga2deg,sga2deg_test)
    path_sga2deg = '/usr1/public/yifeng/pathway_patient/sga2deg_remain.examples'
    save2txt(path_sga2deg,sga2deg_remain)





    i = 0
    j = 0
    path_all = '/usr1/public/yifeng/pathway_patient/examples_train'
    print 'saving to {}...'.format(path_all)
    with io.open(path_all,'w') as file:
        for _, sga in enumerate(sga2deg_list_train):
            deg = sga2deg_list_train[sga]
            file.write(u'pathTo(%s,Y)'%sga)
            # TODO:
            for gene in deg_corpus:
                # TODO:
                if gene in deg:
                    file.write(u'\t+')
                    i += 1
                else:
                    file.write(u'\t-')
                    j += 1
                file.write(u'pathTo(%s,%s)'%(sga,gene))
            file.write(u'\n')

    print 'len(pos) = {}, len(neg) = {}'.format(i,j)
    examples = []
    for line in open(path_all, 'r'):
        line = line.strip()
        examples.append(line)

    print 'len(samples_train) = {}'.format(len(examples))

    SEED = 666
    random.seed(SEED)
    random.shuffle(examples)

    path_train = '/usr1/public/yifeng/pathway_patient/train.examples'
    save2txt_list(path_train,examples)


    i = 0
    j = 0
    path_all = '/usr1/public/yifeng/pathway_patient/examples_test'
    print 'saving to {}...'.format(path_all)
    with io.open(path_all,'w') as file:
        for _, sga in enumerate(sga2deg_list_test):
            deg = sga2deg_list_test[sga]
            file.write(u'pathTo(%s,Y)'%sga)
            # TODO:
            for gene in deg_corpus:
                # TODO:
                if gene in deg:
                    file.write(u'\t+')
                    i += 1
                else:
                    file.write(u'\t-')
                    j += 1
                file.write(u'pathTo(%s,%s)'%(sga,gene))
            file.write(u'\n')

    print 'len(pos) = {}, len(neg) = {}'.format(i,j)
    examples = []
    for line in open(path_all, 'r'):
        line = line.strip()
        examples.append(line)

    print 'len(samples_test) = {}'.format(len(examples))

    SEED = 666
    random.seed(SEED)
    random.shuffle(examples)

    path_test = '/usr1/public/yifeng/pathway_patient/test.examples'
    save2txt_list(path_test,examples)


    i = 0
    j = 0
    path_all = '/usr1/public/yifeng/pathway_patient/examples_remain'
    print 'saving to {}...'.format(path_all)
    with io.open(path_all,'w') as file:
        for _, sga in enumerate(sga2deg_list_remain):
            deg = sga2deg_list_remain[sga]
            file.write(u'pathTo(%s,Y)'%sga)
            # TODO:
            for gene in deg_corpus:
                # TODO:
                if gene in deg:
                    file.write(u'\t+')
                    i += 1
                else:
                    file.write(u'\t-')
                    j += 1
                file.write(u'pathTo(%s,%s)'%(sga,gene))
            file.write(u'\n')

    print 'len(pos) = {}, len(neg) = {}'.format(i,j)
    examples = []
    for line in open(path_all, 'r'):
        line = line.strip()
        examples.append(line)

    print 'len(samples_remain) = {}'.format(len(examples))

    SEED = 666
    random.seed(SEED)
    random.shuffle(examples)

    path_remain = '/usr1/public/yifeng/pathway_patient/remain.examples'
    save2txt_list(path_remain,examples)

    # path_test = '/usr1/public/yifeng/pathway_patient/test.examples'
    # path_remain = '/usr1/public/yifeng/pathway_patient/remain.examples'

    # save2txt_list(path_test,test)
    # save2txt_list(path_remain,remain)

    print 'Done!'


