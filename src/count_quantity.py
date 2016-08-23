# Extract positive grounded examples.
from collections import defaultdict as dd
import io
import os
import random
import argparse

def readsga2deg(path):
    truth = set()
    deg = set()
    sga = set()
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        src = values[0]
        dst = values[1]
        truth.add((values[0],values[1]))
        deg.add(values[1])
        sga.add(values[0])
    #print truth, len(truth)
    return truth,deg,sga




if __name__ == '__main__':
    
    dest = '../pathway_forw_patient'
    

    train,deg_train,sga_train = readsga2deg(dest+'/pathway_origin/sga2deg_train')
    test,deg_test,sga_test = readsga2deg(dest+'/pathway_origin/sga2deg_test')
    remain,deg_remain,sga_remain = readsga2deg(dest+'/pathway_origin/sga2deg_remain')
    
    print len(train),len(test),len(remain)
    print len(train.intersection(test)),len(train.intersection(remain))

    print len(sga_train),len(sga_test),len(sga_remain)
    print len(sga_train.intersection(sga_test)),len(sga_train.intersection(sga_remain))

    print len(deg_train),len(deg_test),len(deg_remain)
    print len(deg_train.intersection(deg_test)),len(deg_train.intersection(deg_remain))

    # precision = 1.0*len(pred.intersection(truth))/len(pred)
    # recall = 1.0*len(pred.intersection(truth))/len(truth)

    # print 'prec = {}, recall = {}'.format(precision,recall)
    # print len(pred.intersection(truth))
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