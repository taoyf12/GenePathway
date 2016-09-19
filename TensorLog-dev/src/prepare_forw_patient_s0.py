# common step for all the following steps. 
# almost do not need change.

# Prepare date from raw data.
# prepare_forw_patient.py: separate the train, test dataset, and produce graph
# in a patient-wise manner.
from collections import defaultdict as dd
import io
import os
import random

# sga2deg_pat_all.graph:  tuples of (pat,SGA,DEG,prob) in different patients.
# pathway_prob.graph:     tuples of (SGA,DEG,prob) united in all patients.
# pathway_occr.graph:     tuples of (SGA,DEG,occr) united in all patients.
# isDEG.cfacts:           facts from original dataset.
# isSGA.cfacts:           facts from original dataset.

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
                    sga2deg.append((row[pos_patient],row[pos_sga],row[pos_deg],row[pos_prob]))
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

    print 'extracting datasets in patient-wise manner...'

    root = '/usr1/public/yifeng/GenePathway'
    dest = root+'/pathway_forw_patient'
    if not os.path.exists(dest):
        os.makedirs(dest)
        os.makedirs(dest+'/pathway_origin')
        os.makedirs(dest+'/pathway_ground')
        os.makedirs(dest+'/pathway_processed')


    # Read raw data from dumped .sql files.
    path_tdi = root+'/TDI_dump/TDI_Results.sql'
    path_sga = root+'/TDI_dump/SGAs.sql'
    path_deg = root+'/TDI_dump/DEGs.sql'
    path_gen = root+'/TDI_dump/Genes.sql'

    patid2sgaid2degid2prob = readTDI_tuple(path_tdi,1,2,4,5)
    sgaid2genid = readSQL(path_sga,0,2)
    degid2genid = readSQL(path_deg,0,2)
    genid2gen = readSQL(path_gen,0,1)


    # isDEG.cfacts
    deg_corpus = set()
    for _, genid in degid2genid.iteritems():
        gene = genid2gen[genid][1:-1].lower()
        deg_corpus.add(gene)

    path_deg = dest+'/pathway_processed/isDEG_all.cfacts'
    print 'saving to {}...'.format(path_deg)
    f = open(path_deg,'w')
    for gene in deg_corpus:
        print >> f, 'isDEG\t'+gene
    f.close
    print 'len(deg_corpus) = {}'.format(len(deg_corpus))

    # isSGA.cfacts
    sga_corpus = set()
    for _, genid in sgaid2genid.iteritems():
        if genid == 'NULL': continue
        gene = genid2gen[genid][1:-1].lower()
        sga_corpus.add(gene)

    path_sga = dest+'/pathway_processed/isSGA_all.cfacts'
    print 'saving to {}...'.format(path_sga)
    f = open(path_sga,'w')
    for gene in sga_corpus:
        print >> f, 'isSGA\t'+gene
    f.close
    print 'len(sga_corpus) = {}'.format(len(sga_corpus))


    print 'mapping from ids to genes...'
    sga2deg_all = list()

    for row in patid2sgaid2degid2prob:
        patid = row[0]
        sgaid_tmp = sgaid2genid[row[1]]
        degid_tmp = degid2genid[row[2]]
        # prob = float(row[3])
        prob = row[3]
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
            sga2deg_all.append((patid,sga,deg,prob))


    path_sga2deg = dest+'/pathway_processed/pathway_pat_all.graph'
    save2txt(path_sga2deg, sga2deg_all)

    print 'len(sga2deg_all) = {}'.format(len(sga2deg_all))

    print 'Done!'
    # Q.E.D.