# Extract positive grounded examples.
from collections import defaultdict as dd
import io
import os
import random
import argparse

def readpathway(path, pos_src, pos_dst):
    print 'reading from: {}...'.format(path)

    lut = dd(list)
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        #print values
        lut[values[1]].append(values[2])

    return lut

def readtruth(path):
    #truth = dd(int)
    truth = {}
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        src = values[0]
        dst = values[1]
        truth[(values[0],values[1])] = 100
        #print truth.keys()
    return truth

def myiter(truth, lut, src, src_origin, maxcount, count):
    count += 1
    tmp = {}
    for i in truth.keys():
        tmp[i] = truth[i]
    truth = {}
    for i in tmp.keys():
        truth[i] = tmp[i]

    if count == 5: return truth
    for dst in lut[src]:
        # if (src_origin, dst) not in truth: continue
        if (src_origin, dst) in truth.keys():
            # print (src_origin,dst)
            tmp = truth[(src_origin,dst)]
            if count < tmp:
                truth[(src_origin,dst)] = count
        src = dst
        #truth = dd(int)
        truth = myiter(truth, lut, src, src_origin, maxcount, count)

def count_jump(truth, lut, maxcount):
    src_set = set()
    for t in truth:
        src_set.add(t[0])
    for src_origin in src_set:
        src = src_origin
        count = 0
        truth = myiter(truth, lut, src, src_origin, maxcount, count)
    return truth


if __name__ == '__main__':
    
    dest = '../pathway_forw_patient'

    lut = readpathway(dest+'/pathway_ground/pathway.graph', 1, 2)


    truth = readtruth(dest+'/pathway_ground/sga2deg_remain')

    jump = count_jump(truth, lut, 5)

    for t in jump.keys():
        print t, jump[t]


    print 'Done!'
    # Q.E.D.