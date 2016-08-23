# Extract positive grounded examples.
from collections import defaultdict as dd
import io
import os
import random
import argparse

def isclose(a, b, rel_tol=1e-6):
    return (abs(a-b) <= rel_tol)

def predict(path, pos_start):
    print 'reading from: {}...'.format(path)
    src2dst = set()
    #src2dst = []
    src_tmp,dst_tmp = 'src_tmp','dst_tmp'
    prob_tmp = 0.0
    flag = '0'
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        #print values
        if '#' in values[0]:
            flag = '1'
            continue
        prob = values[1]
        val = values[-1][:-1]
        val = val[pos_start:-1]
        val = val.split(',')
        src,dst = val[0], val[1]
        prob = float(prob)

        if flag == '1':
            src_tmp,dst_tmp,prob_tmp = src,dst,prob
            src2dst.add((src,dst))
            flag = '2'
        elif flag == '2': # possiblity1: a new src; possibility2: continued src
            # obviously, src == src_tmp:
            if isclose(prob, prob_tmp):
                src2dst.remove((src_tmp,dst_tmp))
            # else:
            # do nothing
            flag = '3'
        elif flag == '3':
            continue
        # if src == src_tmp:
        #     if flag == 'top1':
        #         flag = 'nottop1'
        #         if isclose(prob,prob_tmp) == True:
        #             src2dst.remove((src_tmp,dst_tmp))
        #     src_tmp,dst_tmp = src,dst
        #     prob_tmp = prob
        # else:
        #     src_tmp,dst_tmp = src,dst
        #     prob_tmp = prob
        #     flag = 'top1'
        #     src2dst.add((src_tmp,dst_tmp))
        #     #src2dst.append((val[0],val[1]))
        # #print val
        # #print prob,val
    print src2dst
    print 'len(src2dst) = {}'.format(len(src2dst))
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