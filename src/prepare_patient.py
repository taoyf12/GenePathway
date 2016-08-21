# Prepare date from raw data.
# prepare_patient.py: separate the train, test, remain data set
# in a patient-wise manner.
from collections import defaultdict as dd
import io
import os
import random

def readTDI_tuple(path, pos_patient, pos_sga, pos_deg):
    '''
    Collect all the (patient_id, sgaid, degid) tuples.
    path: dir of .sql file.
    pos_patient: position of patid.
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

def writeSample(path, filename, sga2deglist, deg_corpus):
    print 'saving to {}...'.format(path+'/'+filename)
    #i,j = 0,0
    with io.open(path+'/tmp','w') as file:
        for _, sga in enumerate(sga2deglist):
            deg = sga2deglist[sga]
            file.write(u'pathTo(%s,Y)'%sga)
            # TODO:
            for gene in deg_corpus:
                # TODO:
                if gene in deg:
                    file.write(u'\t+')
                    #i += 1
                else:
                    file.write(u'\t-')
                    #j += 1
                file.write(u'pathTo(%s,%s)'%(sga,gene))
            file.write(u'\n')

    #print 'len(pos) = {}, len(neg) = {}'.format(i,j)

    examples = []
    for line in open(path+'/tmp', 'r'):
        line = line.strip()
        examples.append(line)

    print 'len(samples) = {}'.format(len(examples))

    SEED = 666
    random.seed(SEED)
    random.shuffle(examples)
    os.remove(path+'/tmp');
    path_out = path+'/'+filename
    save2txt_list(path_out,examples)

if __name__ == '__main__':
    print 'generating datasets in patient-wise manner...'

    dest = '../pathway_patient'
    if not os.path.exists(dest):
        os.makedirs(dest)
        os.makedirs(dest+'/pathway_origin')
        os.makedirs(dest+'/pathway_ground')



    # Extract (sga, deg) pairs from dumped .sql file.
    # Randomly generate train, test and remain set.
    NUM_PAT = 4468
    patid_list = range(1,NUM_PAT+1)
    SEED = 888
    random.seed(SEED)
    random.shuffle(patid_list)

    thresh1 = 0.1
    thresh2 = 0.2
    cut1 = int(thresh1*NUM_PAT)
    cut2 = int(thresh2*NUM_PAT)
    patid_train = patid_list[0:cut1]
    patid_test = patid_list[cut1:cut2]
    patid_remain = patid_list[cut2:NUM_PAT]


    path_tdi = '../TDI_dump/TDI_Results.sql'
    path_sga = '../TDI_dump/SGAs.sql'
    path_deg = '../TDI_dump/DEGs.sql'
    path_gen = '../TDI_dump/Genes.sql'

    patid2sgaid2degid = readTDI_tuple(path_tdi,1,2,4)
    sgaid2genid = readSQL(path_sga,0,2)
    degid2genid = readSQL(path_deg,0,2)
    genid2gen = readSQL(path_gen,0,1)



    # prepare the files required by ProPPR.
    # pathway.graph
    path_pathway = '../TDI_dump/pathway.cfacts'
    corpus, pathway = buildPathway(path_pathway)
    path_pathway_out = dest+'/pathway_origin/pathway.graph'
    save2txt(path_pathway_out, pathway)
    # labels.cfacts
    deg_corpus = set()
    for _, genid in degid2genid.iteritems():
        gene = genid2gen[genid][1:-1].lower()
        if gene in corpus:
            deg_corpus.add(gene)
        #genid2gen = readSQL(path_gen,0,1)

    path_label = dest+'/pathway_origin/labels.cfacts'
    print 'saving to {}...'.format(path_label)
    f = open(path_label,'w')
    for gene in deg_corpus:
        print >> f, 'isDEG\t'+gene
    f.close
    print 'len(deg) = {}'.format(len(deg_corpus))


    print 'mapping from ids to genes...'
    sga2deg_train = set()
    sga2deg_test = set()
    sga2deg_remain = set()
    # need to be included in the graph, if used.
    # sga2deg = set()
    for row in patid2sgaid2degid:
        patid = row[0]
        sgaid_tmp = sgaid2genid[row[1]]
        degid_tmp = degid2genid[row[2]]
        #print patid
        # sga is unit, no corresponding genid.
        if sgaid_tmp == 'NULL': continue
        sga = genid2gen[sgaid_tmp]
        deg = genid2gen[degid_tmp]
        # normalize to lower case gene representation.
        sga = sga[1:-1].lower()
        deg = deg[1:-1].lower()
        # TODO:
        # sga and deg should be different.
        if sga != deg:
            # sga2deg.add((sga,deg))
            if patid in patid_train:
                sga2deg_train.add((sga,deg))
            elif patid in patid_test:
                sga2deg_test.add((sga,deg))
            else: # elif patid in patid_remain:
                sga2deg_remain.add((sga,deg))


    # (sga,deg) pairs within the pathway.graph
    sga2deg_out_train = set()
    sga2deg_out_test = set()
    sga2deg_out_remain = set()    
    for values in sga2deg_train:
        genex = values[0]
        geney = values[1]
        if (genex in corpus) and (geney in corpus):
            # genex and geney won't be same, we have examined it before.
            sga2deg_out_train.add((genex,geney))
    for values in sga2deg_test:
        genex = values[0]
        geney = values[1]
        if (genex in corpus) and (geney in corpus):
            sga2deg_out_test.add((genex,geney))
    for values in sga2deg_remain:
        genex = values[0]
        geney = values[1]
        if (genex in corpus) and (geney in corpus):
            sga2deg_out_remain.add((genex,geney))

    sga2deg_train = sga2deg_out_train
    sga2deg_test = sga2deg_out_test
    sga2deg_remain = sga2deg_out_remain

    path_sga2deg = dest+'/pathway_origin/sga2deg_train'
    save2txt(path_sga2deg,sga2deg_train)
    path_sga2deg = dest+'/pathway_origin/sga2deg_test'
    save2txt(path_sga2deg,sga2deg_test)
    path_sga2deg = dest+'/pathway_origin/sga2deg_remain'
    save2txt(path_sga2deg,sga2deg_remain)

    print 'len(sga2deg_train) = {}'.format(len(sga2deg_train))
    print 'len(sga2deg_test) = {}'.format(len(sga2deg_test))
    print 'len(sga2deg_remain) = {}'.format(len(sga2deg_remain))


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

    writeSample(dest+'/pathway_origin', 'train.examples', sga2deg_list_train, deg_corpus)
    writeSample(dest+'/pathway_origin', 'test.examples', sga2deg_list_test, deg_corpus)
    writeSample(dest+'/pathway_origin', 'remain.examples', sga2deg_list_remain, deg_corpus)

    print 'Done!'
    # Q.E.D.