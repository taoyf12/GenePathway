# Prepare date from raw data.
# prepare_forw_patient.py: separate the train, test dataset, and produce graph
# in a patient-wise manner.
from collections import defaultdict as dd
import io
import os
import random

# prepare the data for our experiments.

def readTDI_tuple(path, pos_patient, pos_sga, pos_deg, pos_prob):
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
                    sga2deg.append((int(row[pos_patient]),row[pos_sga],row[pos_deg],row[pos_prob]))
    print 'len(patid2sgaid2degid2prob) = {}'.format(len(sga2deg))
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

def extract_sga2deg(path_sga2deg_all,path_sga2deg_train,thresh):
    print 'reading from: {}...'.format(path_sga2deg_all)
    sga2deg = []
    sga2deg_str = []
    sga_corpus = set()
    deg_corpus = set()
    for line in open(path_sga2deg_all, 'r'):
        values = line.strip().split('\t')
        sga,deg,prob = values[1],values[2],float(values[3])
        if prob > thresh:
            sga2deg.append((sga,deg,prob))
            sga_corpus.add(sga)
            deg_corpus.add(deg)
            sga2deg_str.append('\t'.join(values))

    print 'saving to {}...'.format(path_sga2deg_train)
    f = open(path_sga2deg_train,'w')
    for row in sga2deg_str:
        print >> f, row
    f.close
    return sga2deg,sga_corpus,deg_corpus

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

if __name__ == '__main__':

    print 'preparing training set'

    root = '/usr1/public/yifeng/GenePathway'
    dest = root+'/pathway_forw_patient'


    # Read raw data from dumped .sql files.

    path_sga2deg_all = dest+'/pathway_processed/pathway_prob.graph'
    path_sga2deg_train = dest+'/pathway_origin/pathway.graph'
    thresh = 0.8
    sga2deg,sga_corpus,deg_corpus = extract_sga2deg(path_sga2deg_all,path_sga2deg_train,thresh)
    print len(sga2deg),len(sga_corpus),len(deg_corpus)









    # # isDEG.cfacts
    # deg_corpus = set()
    # for _, genid in degid2genid.iteritems():
    #     gene = genid2gen[genid][1:-1].lower()
    #     deg_corpus.add(gene)

    # path_deg = dest+'/pathway_processed/isDEG.cfacts'
    # print 'saving to {}...'.format(path_deg)
    # f = open(path_deg,'w')
    # for gene in deg_corpus:
    #     print >> f, 'isDEG\t'+gene
    # f.close
    # print 'len(deg) = {}'.format(len(deg_corpus))

    # # isSGA.cfacts
    # sga_corpus = set()
    # for _, genid in sgaid2genid.iteritems():
    #     if genid == 'NULL': continue
    #     gene = genid2gen[genid][1:-1].lower()
    #     sga_corpus.add(gene)

    # path_sga = dest+'/pathway_processed/isSGA.cfacts'
    # print 'saving to {}...'.format(path_sga)
    # f = open(path_sga,'w')
    # for gene in sga_corpus:
    #     print >> f, 'isSGA\t'+gene
    # f.close
    # print 'len(sga) = {}'.format(len(sga_corpus))


    # print 'mapping from ids to genes...'
    # sga2deg_all = list()

    # for row in patid2sgaid2degid2prob:
    #     patid = row[0]
    #     sgaid_tmp = sgaid2genid[row[1]]
    #     degid_tmp = degid2genid[row[2]]
    #     # prob = float(row[3])

    #     # sga is unit, no corresponding genid.
    #     if sgaid_tmp == 'NULL': continue
    #     sga = genid2gen[sgaid_tmp]
    #     deg = genid2gen[degid_tmp]
    #     # normalize to lower case gene representation.
    #     sga = sga[1:-1].lower()
    #     deg = deg[1:-1].lower()

    #     # TODO:
    #     # sga and deg should be different.
    #     if sga != deg:
    #         sga2deg_all.append((patid,sga,deg,prob))


    # path_sga2deg = dest+'/pathway_processed/pathway_pat_all.graph'
    # save2txt(path_sga2deg, sga2deg_all)

    # print 'len(sga2deg_all) = {}'.format(len(sga2deg_all))
    print 'Done!'
    # Q.E.D.