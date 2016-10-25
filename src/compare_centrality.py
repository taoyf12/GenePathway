# generate in the way of weight(SGA -> DEG) = \sum (posterior prob) / Number_of_tumors_with_SGA
from collections import defaultdict as dd
import io
import os
import random


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
    
# TODO: consider the weight of edges.
# consider the averaged effect.    
if __name__ == '__main__':

    #print 'calculating centrality...'

    root = '/usr1/public/yifeng/GenePathway'


    deg_corpus = set()
    path_deg = root+'/TensorLog-dev/src/pathway/pathway_processed/isDEG_all.cfacts'
    print 'reading from: {}...'.format(path_deg)
    for line in open(path_deg, 'r'):
        values = line.strip().split('\t')
        isdeg,deg = values[0],values[1]
        deg_corpus.add(deg)
        # sga_corpus.add(values[0])
        # deg_corpus.add(values[1])
        # sga2deg[values[0]].add(values[1])
    # print sga2deg
    print 'len(deg_corpus) = {}'.format(len(deg_corpus))














    #dest = root+'/pathway'
    gene2cent = dd(str)
    path_centrality = root+'/src/betweenness'


    # path_sga2deg = dest+'/remain'

    # # sga,deg,dist
    # sga_corpus = set()
    # deg_corpus = set()
    # sga2deg = dd(set)

    # dist = dd(float)
    # center = dd(str)





    print 'reading from: {}...'.format(path_centrality)
    for line in open(path_centrality, 'r'):
        values = line.strip().split('\t')
        gene,cent = values[0],values[1]
        gene2cent[gene] = cent
        # sga_corpus.add(values[0])
        # deg_corpus.add(values[1])
        # sga2deg[values[0]].add(values[1])
    # print sga2deg
    print 'len(gene2cent) = {}'.format(len(gene2cent))

    # shortpath = list()

    # 
    gene2dst = dd(str)
    path_params = root+'/TensorLog-dev/src/pathway_1023/trial032/params.out'
    print 'reading from {}...'.format(path_params)
    for line in open(path_params, 'r'):
        values = line.strip().split('\t')
        if values[0] == 'dst':
            gene,dst = values[1],values[2]
            gene2dst[gene] = dst
    print 'len(gene2dst) = {}'.format(len(gene2dst))



    gene2src = dd(str)

    for line in open(path_params, 'r'):
        values = line.strip().split('\t')
        if values[0] == 'src':
            gene,src = values[1],values[2]
            gene2src[gene] = src
    print 'len(gene2src) = {}'.format(len(gene2src))


    path_compare = root+'/src/compare_src_new'
    f = open(path_compare, 'w')
    for gene in gene2src:
        if gene in gene2cent:
            print >> f, gene + '\t' + gene2cent[gene] + '\t' + gene2src[gene]
        else:
            print >> f, gene + '\t' + '0.0' + '\t' + gene2src[gene]
    # for gene,cent in gene2cent.iteritems():
    #     if gene in gene2src:
    #         print >> f, gene + '\t' + cent + '\t' + gene2src[gene]

    f.close()

    path_compare = root+'/src/compare_dst_new'
    f = open(path_compare, 'w')
    # gene2dst
    for gene in gene2src:
        if gene in gene2cent:
            print >> f, gene + '\t' + gene2cent[gene] + '\t' + gene2dst[gene]
        else:
            print >> f, gene + '\t' + '0.0' + '\t' + gene2dst[gene]
        #else:


    f.close()

    print 'Done!'
# Q.E.D.
