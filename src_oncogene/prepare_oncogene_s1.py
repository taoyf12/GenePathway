# prepare the data for sga2deg relation.
from collections import defaultdict as dd
import io
import os
import random

if __name__ == '__main__':

    print 'preparing drives relation...'

    root = '/usr1/public/yifeng/GenePathway'
    dest = root+'/oncogene'

    path_sga2deg_all = dest+'/oncogene_processed/pathway_pat_all.graph'

    print 'reading from: {}...'.format(path_sga2deg_all)

    sga2deg = dd(float)

    count = 0
    for line in open(path_sga2deg_all, 'r'):
        count += 1
        if count%1000000 == 0:
            print count
        values = line.strip().split('\t')
        patid,sga,deg,prob = int(values[0]),values[1],values[2],float(values[3])
        sga2deg[(sga,deg)] += prob

    path_graph = dest+'/sga2deg.graph'
    print 'saving to {}...'.format(path_graph)
    f = open(path_graph,'w')
    for row in sga2deg.keys():
        sga,deg,prob = row[0],row[1],str(sga2deg[row])
        print >> f, 'sga2deg\t'+sga+'\t'+deg+'\t'+prob
    f.close

    print 'Done!'
# Q.E.D.
