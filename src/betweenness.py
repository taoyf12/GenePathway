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

    print 'calculating centrality...'

    root = '/usr1/public/yifeng/GenePathway'
    dest = root+'/pathway'

    path_sga2deg = dest+'/remain'

    # sga,deg,dist
    sga_corpus = set()
    deg_corpus = set()
    sga2deg = dd(set)

    dist = dd(float)
    center = dd(str)

    print 'reading from: {}...'.format(path_sga2deg)

    for line in open(path_sga2deg, 'r'):
        values = line.strip().split('\t')
        sga_corpus.add(values[0])
        deg_corpus.add(values[1])
        sga2deg[values[0]].add(values[1])
    # print sga2deg

    # shortpath = list()

    # 
    print 'counting shortest path...'
    gv = dd(float)

    j = 0
    for sga in sga_corpus:
        j += 1
        if j%100 == 0:
            
            # print gv
            print j
            print len(gv)
        #if j >= 200: break
        for deg in deg_corpus:
            # the nodes are directly connected.
            if deg in sga2deg[sga]: continue
            i = 0
            for v in sga2deg[sga]:
                if v == deg: continue
                if deg in sga2deg[v]: i += 1
            for v in sga2deg[sga]:
                if v == deg: continue
                if deg in sga2deg[v]: gv[v] += 1.0/i



    # print 'counting shortest path...'
    # i = 0
    # for sga in sga_corpus:
    #     i += 1
    #     if i%1000 == 0:
    #         print i
    #     for vcom in sga2deg[sga]:
    #         v = vcom[0]
    #         d1 = vcom[1]
    #         #print vcom
    #         for degcom in sga2deg[v]:
    #             deg  =degcom[0]
    #             d2 = degcom[1]
    #             if dist[(sga,deg)] == 0:
    #                 dist[(sga,deg)] = 1000000000
    #             if (d1+d2) < dist[(sga,deg)]:
    #                 dist[(sga,deg)] = d1+d2
    #                 center[(sga,deg)] = v


    # gv = dd(float)
    # for k,v in center.iteritems():
    #     gv[v] += 1

    
    #print 'saving to {}'%format(path_betweenness)

    path_betweenness = root+'/src/betweenness'
    f = open(path_betweenness, 'w')
    for v,val in gv.iteritems():
        print >> f, v+'\t'+str(val)

    f.close()
    print 'Done!'
# Q.E.D.
