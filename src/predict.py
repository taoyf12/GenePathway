# Extract positive grounded examples.
from collections import defaultdict as dd
import io
import os
import random
import argparse

def predict(path, pos_start):
    print 'reading from: {}...'.format(path)
    src2dst = set()
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        #print values
        if '#' in values[0]: continue
        prob = values[1]
        val = values[-1][:-1]
        val = val[pos_start:-1]
        val = val.split(',')
        # sga.add(val[1])
        src2dst.add((val[0],val[1]))
        #print val
        print type(prob),val
    print 'len(src2dst_all) = {}'.format(len(src2dst))
    return src2dst

if __name__ == '__main__':
    
    dest = '../pathway_forw_patient'
    relation = 'pathTo'
    pos_start = len(relation) + 1
    pred = predict(dest+'/pathway_ground/test.solutions.txt', pos_start)





    # src_train,dst_train,src2dst_train = extract_ground_in(dest+'/pathway_origin/train.solutions.txt', \
    #     dest+'/pathway_origin/sga2deg_train', dest+'/pathway_ground/train.examples', 'pathTo', \
    #     True, dest+'/pathway_ground/labels.cfacts', 'isDEG')
    # src_test,dst_test,src2dst_test = extract_ground_in(dest+'/pathway_origin/test.solutions.txt', \
    #     dest+'/pathway_origin/sga2deg_test', dest+'/pathway_ground/test.examples', 'pathTo', \
    #     False)
    # src_remain,dst_remain,src2dst_remain = extract_ground_in(dest+'/pathway_origin/remain.solutions.txt', \
    #     dest+'/pathway_origin/sga2deg_remain', dest+'/pathway_ground/remain.examples', 'pathTo', \
    #     False)
    # show_intersection('size of sga corpus:', src_train, src_test, src_remain)
    # show_intersection('size of deg corpus:', dst_train, dst_test, dst_remain)
    # show_intersection('size of sga2deg:', src2dst_train, src2dst_test, src2dst_remain)

    print 'Done!'
    # Q.E.D.