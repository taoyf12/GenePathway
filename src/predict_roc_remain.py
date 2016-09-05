# Extract positive grounded examples.
from collections import defaultdict as dd
import io
import os
import random
import argparse

def predict(path, pos_start, k):
    #print 'reading from: {}...'.format(path)
    src2dst = set()
    #src2dst = []
    src_tmp,dst_tmp = 'src_tmp','dst_tmp'
    prob_tmp = 0.0
    flag = 0
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        #print values
        if '#' in values[0]:
            flag = 1
            continue
        prob = values[1]
        val = values[-1][:-1]
        val = val[pos_start:-1]
        val = val.split(',')
        src,dst = val[0], val[1]
        prob = float(prob)

        T = k+1
        if flag == 1:
            src_tmp,dst_tmp,prob_tmp = src,dst,prob
            src2dst.add((src,dst))
            flag = flag + 1
        elif flag <= T-1: # possiblity1: a new src; possibility2: continued src
            # obviously, src == src_tmp:
            src_tmp,dst_tmp,prob_tmp = src,dst,prob
            src2dst.add((src,dst))
            # else:
            # do nothing
            flag = flag + 1
        elif flag == T:
            continue
    # print src2dst
    # print 'len(src2dst) = {}'.format(len(src2dst))
    return src2dst

def readtruth(path):
    truth = set()
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        src = values[0]
        dst = values[1]
        truth.add((src,dst))
    #print truth, len(truth)
    return truth


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

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', help = 'name of output file', type = str, default = 'eps=1e-4')
    args = parser.parse_args()

    print 'evaluating...'
    print 'top@k\tprec\t\trecall'


    root = '/usr1/public/yifeng/GenePathway'
    dest = root+'/pathway_forw_patient'

    relation = 'pathTo'
    pos_start = len(relation) + 1

    KSet = [1,2,3,4,5,10,20,50,100,200,500,1000,2000,4000,8000]

    roc = list()
    for k in KSet:
        pred = predict(dest+'/pathway_origin/remain.solutions.txt', pos_start,k)

        truth = readtruth(dest+'/pathway_origin/remain')

        precision = 1.0*len(pred.intersection(truth))/len(pred)
        recall = 1.0*len(pred.intersection(truth))/len(truth)

        print '{}\t{}\t{}'.format(k,precision,recall)
        roc.append((str(k),str(precision),str(recall)))

    path_roc = root+'/src/'+args.filename
    save2txt(path_roc,roc)
    print 'Done!'
    # Q.E.D.