# Prepare date from raw data.
# prepare_forw_patient.py: separate the train, test dataset, and produce graph
# in a patient-wise manner.
from collections import defaultdict as dd
import io
import os
import random

# check
# extract real SGA corpus, DEG corpus.

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

def readpathway(path_pathway):
    print 'reading from: {}...'.format(path_pathway)
    sga2deg2prob,sga2deg2occr = dd(float),dd(int)
    for line in open(path_pathway, 'r'):
        values = line.split('\t')
        values[-1] = values[-1][:-1]
        #print values
        sga = values[1]
        deg = values[2]
        prob = float(values[3])
        sga2deg2prob[('leadTo',sga,deg)] += prob
        sga2deg2occr[('leadTo',sga,deg)] += 1
    print 'len = {},{}'.format(len(sga2deg2prob),len(sga2deg2occr))
    return sga2deg2prob,sga2deg2occr

def readcorpus(path):
    print 'reading from: {}...'.format(path)
    corpus = set()
    for line in open(path,'r'):
        values = line.strip().split('\t')
        #print values
        corpus.add(values[1])
    return corpus



if __name__ == '__main__':

    print 'checking if corpus contain pathway...'

    root = '/usr1/public/yifeng/GenePathway'
    dest = root+'/pathway_forw_patient'
    path_curt = dest+'/pathway_processed'


    # Combine pathways.
    path_pathway = path_curt+'/pathway_pat_all.graph'

    sga2deg2prob,sga2deg2occr = readpathway(path_pathway)

    path_prob = path_curt+'/pathway_prob.graph'
    path_occr = path_curt+'/pathway_occr.graph'

    sga2deg2prob_list,sga2deg2occr_list = list(),list()
    for row in sga2deg2prob.keys():
        sga2deg2prob_list.append([row[0],row[1],row[2],str(sga2deg2prob[row])])
    for row in sga2deg2occr.keys():
        sga2deg2occr_list.append([row[0],row[1],row[2],str(sga2deg2occr[row])])

    save2txt(path_prob,sga2deg2prob_list)
    save2txt(path_occr,sga2deg2occr_list)

    path_sga_all = path_curt+'/isSGA_all.cfacts'
    path_deg_all = path_curt+'/isDEG_all.cfacts'

    sga_corpus_all = readcorpus(path_sga_all)
    deg_corpus_all = readcorpus(path_deg_all)

    path_sga = path_curt+'/isSGA.cfacts'
    path_deg = path_curt+'/isDEG.cfacts'

    sga_corpus = set()
    deg_corpus = set()

    for row in sga2deg2occr.keys():
        sga = row[1]
        deg = row[2]
        sga_corpus.add(sga)
        deg_corpus.add(deg)

    print 'saving to {}...'.format(path_sga)
    f = open(path_sga,'w')
    for gene in sga_corpus:
        print >> f, 'isSGA\t'+gene
    f.close
    print 'len(sga) = {}'.format(len(sga_corpus))

    print 'saving to {}...'.format(path_deg)
    f = open(path_deg,'w')
    for gene in deg_corpus:
        print >> f, 'isDEG\t'+gene
    f.close
    print 'len(deg) = {}'.format(len(deg_corpus))


    print len(sga_corpus.intersection(sga_corpus_all)), \
    len(deg_corpus.intersection(deg_corpus_all))

    print len(sga_corpus.intersection(deg_corpus)), \
    len(sga_corpus.union(deg_corpus)), \
    len(sga_corpus_all.intersection(deg_corpus_all)), \
    len(sga_corpus_all.union(deg_corpus_all))

    print 'Done!'
    # Q.E.D.