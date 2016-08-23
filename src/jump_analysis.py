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
        truth[(values[0],values[1])] = 1000
        #print truth.keys()
    return truth


def bfs(truth, lut):
    dist = {}
    # distance from root to each node.
    #i = 0
    for t in truth.keys():
        #i += 1
        #if i == 2: break
        #print t
        dist = {}
        src = t[0]
        dst = t[1]
        queue = list()
        queue.append(src)
        dist[src] = 0
        #print src, dst
        flag = 0
        while len(queue) != 0:
            if flag == 1:
                flag = 0
                break
            current = queue[0]
            #print queue
            queue = queue[1:]
            for n in lut[current]:
                dist[n] = dist[current] + 1
                queue.append(n)
                #print n
                if n == dst:
                    truth[(src,dst)] = dist[n]
                    flag = 1
                    break
    return truth







    # src_set = set()
    # for t in truth:
    #     src_set.add(t[0])
    # for src_origin in src_set:
    #     src = src_origin
    #     count = 0
    #     truth = myiter(truth, lut, src, src_origin, maxcount, count)
    return truth


if __name__ == '__main__':
    
    dest = '../pathway_forw_patient'

    lut = readpathway(dest+'/pathway_ground/pathway.graph', 1, 2)
    truth = readtruth(dest+'/pathway_ground/sga2deg_remain')

    truth = bfs(truth, lut)

    for t in truth.keys():
        print '{}\t{}'.format(t, truth[t])


    print 'Done!'
    # Q.E.D.