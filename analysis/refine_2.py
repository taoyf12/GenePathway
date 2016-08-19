# Refine the data: get the abbreviated graph.
from collections import defaultdict as dd
import io
import random

def readfeatures(path_visit, path_all):

    print 'reading from: {}, {}...'.format(path_visit, path_all)
    set_visit = set()
    set_all = set()
    wt = []
    i = 0
    for line in open(path_visit, 'r'):
        i += 1
        if i == 1: continue
        values = line.strip().split('\t')
        #print values
        if ('id(' in values[0]) or ('db(' in values[0]): continue
        values[0] = values[0][2:-1]
        val = values[0].strip().split(',')
        # print val
        wt.append(float(values[1]))
        set_visit.add((val[0],val[1]))
        set_all.add(('leadTo',val[0],val[1],'1.0000'))
    #print len(set_visit)
    #print set_all
    avg = reduce(lambda x, y: x+y, wt) /len(wt)

    #print avg
    avg = '%.4f' % avg
    avg = '0.0050'
    #print avg
    for line in open(path_all, 'r'):
        values = line.strip().split('\t')
        if (values[1],values[2]) in set_visit: continue
        set_all.add(('leadTo',values[1],values[2],avg))
    print len(set_all)
    return set_all

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

    path_visit = '../pathway_refine/train.params'
    path_all = '../pathway_refine/pathway.graph'
    pathway = readfeatures(path_visit, path_all)

    path_pathway = '../pathway_refine/pathway_trained.graph'
    save2txt(path_pathway, pathway)


    print 'Done!'


