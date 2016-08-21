# Extract positive grounded examples.
from collections import defaultdict as dd
import io
import os
import random
import argparse

def readsolution(path,pos_start):
    '''
    read into (src,dst) tuples from file.
    '''
    print 'reading from: {}...'.format(path)
    # sga = set()
    src2dst_all = set()
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        #print values
        if '#' in values[0]: continue
        val = values[-1][:-1]
        val = val[pos_start:-1]
        val = val.split(',')
        # sga.add(val[1])
        src2dst_all.add((val[0],val[1]))
        #print val
    print 'len(src2dst_all) = {}'.format(len(src2dst_all))
    return src2dst_all

def readsrc2dst(path):
    '''
    read into (sga,deg) tuples from file.
    '''
    print 'reading from: {}...'.format(path)
    src2dst = set()
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        src2dst.add((values[0],values[1]))
    return src2dst

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

def extract_ground_in(path_solution, path_src2dst, path_out, relation, is_train, path_label=None, label_notation=None):
    '''
    extract grounded positive solutions.
    path_solution: *.solutions.txt file, contains grounded examples.
    path_sga2deg: contrain positive (un)grounded positive examples.
    path_out: output file contains grounded positive examples.
    relation: 'pathTo'/'pathFrom'
    is_train: if it is training set.
    path_label: if it is training set, we compress the isDEG/isSGA corpus.
    label_notation: 'isDEG'/'isSGA'
    '''
    # all the grounded examples.
    pos_start = len(relation) + 1
    src2dst_all = readsolution(path_solution,pos_start)
    # positive examples.
    src2dst = readsrc2dst(path_src2dst)
    # positive grounded examples.
    src2dst = src2dst.intersection(src2dst_all)

    dst_corpus = set()
    for pair in src2dst:
        dst_corpus.add(pair[1])

    if is_train:
        print 'saving to {}...'.format(path_label)
        f = open(path_label,'w')
        for gene in dst_corpus:
            # TODO:
            print >> f, label_notation+'\t'+gene
        f.close

    src2dst_list = dd(list)
    for line in src2dst:
        src = line[0]
        dst = line[1]
        src2dst_list[src].append(dst)

    path_all = '../tmp'
    print 'saving to {}...'.format(path_all)
    with io.open(path_all,'w') as file:
        for _, src in enumerate(src2dst_list):
            dst = src2dst_list[src]
            file.write(u'%s(%s,Y)'%(relation,src))
            # TODO:
            for gene in dst_corpus:
                # TODO:
                if gene in dst:
                    file.write(u'\t+')
                else:
                    file.write(u'\t-')
                file.write(u'%s(%s,%s)'%(relation,src,gene))
            file.write(u'\n')

    examples = []
    for line in open(path_all, 'r'):
        line = line.strip()
        examples.append(line)

    # print 'len(samples) = {}'.format(len(examples))

    SEED = 123
    random.seed(SEED)
    random.shuffle(examples)

    os.remove(path_all)

    save2txt_list(path_out,examples)
    return set(src2dst_list.keys()),dst_corpus,src2dst

def show_intersection(intro, train, test, remain):
    print '_'*30
    print intro
    print 'train\ttest\tremain'
    print '{}\t{}\t{}'.format(len(train),len(test),len(remain))
    print 'train&test\ttrain&remain'
    print '{}\t{}'.format(len(train.intersection(test)), len(train.intersection(remain)))

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--direct', help = 'forw/bakw', type = str, default = 'forw')
    args = parser.parse_args()

    if args.direct == 'forw':
        print 'forward!'
        dest = '../pathway_forw_patient'
        src_train,dst_train,src2dst_train = extract_ground_in(dest+'/pathway_origin/train.solutions.txt', \
            dest+'/pathway_origin/sga2deg_train', dest+'/pathway_ground/train.examples', 'pathTo', \
            True, dest+'/pathway_ground/labels.cfacts', 'isDEG')
        src_test,dst_test,src2dst_test = extract_ground_in(dest+'/pathway_origin/test.solutions.txt', \
            dest+'/pathway_origin/sga2deg_test', dest+'/pathway_ground/test.examples', 'pathTo', \
            False)
        src_remain,dst_remain,src2dst_remain = extract_ground_in(dest+'/pathway_origin/remain.solutions.txt', \
            dest+'/pathway_origin/sga2deg_remain', dest+'/pathway_ground/remain.examples', 'pathTo', \
            False)
        show_intersection('size of sga corpus:', src_train, src_test, src_remain)
        show_intersection('size of deg corpus:', dst_train, dst_test, dst_remain)
        show_intersection('size of sga2deg:', src2dst_train, src2dst_test, src2dst_remain)
    elif args.direct == 'bakw':
        print 'backward!'
        dest = '../pathway_bakw_patient'
        src_train,dst_train,src2dst_train = extract_ground_in(dest+'/pathway_origin/train.solutions.txt', \
            dest+'/pathway_origin/deg2sga_train', dest+'/pathway_ground/train.examples', 'pathFrom', \
            True, dest+'/pathway_ground/labels.cfacts', 'isSGA')
        src_test,dst_test,src2dst_test = extract_ground_in(dest+'/pathway_origin/test.solutions.txt', \
            dest+'/pathway_origin/deg2sga_test', dest+'/pathway_ground/test.examples', 'pathFrom', \
            False)
        src_remain,dst_remain,src2dst_remain = extract_ground_in(dest+'/pathway_origin/remain.solutions.txt', \
            dest+'/pathway_origin/deg2sga_remain', dest+'/pathway_ground/remain.examples', 'pathFrom', \
            False)
        show_intersection('size of deg corpus:', src_train, src_test, src_remain)
        show_intersection('size of sga corpus:', dst_train, dst_test, dst_remain)
        show_intersection('size of deg2sga:', src2dst_train, src2dst_test, src2dst_remain)
    print 'Done!'
    # Q.E.D.