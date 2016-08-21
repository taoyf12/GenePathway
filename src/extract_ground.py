# Extract positive grounded examples.
from collections import defaultdict as dd
import io
import os
import random

def readsolution(path):
    '''
    read into (sga,deg) tuples from file.
    '''
    print 'reading from: {}...'.format(path)
    deg = set()
    sga2deg_all = set()
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        #print values
        if '#' in values[0]: continue
        val = values[-1][:-1]
        val = val[7:-1]
        val = val.split(',')
        deg.add(val[1])
        sga2deg_all.add((val[0],val[1]))
        #print val
    print 'len(sga2deg_all) = {}'.format(len(sga2deg_all))
    return sga2deg_all

def readsga2deg(path):
    '''
    read into (sga,deg) tuples from file.
    '''
    print 'reading from: {}...'.format(path)
    sga2deg = set()
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        sga2deg.add((values[0],values[1]))
    return sga2deg

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

def extract_ground_in(path_solution, path_sga2deg, path_out, is_train, path_label=None):
    '''
    extract grounded positive solutions.
    path_solution: *.solutions.txt file, contains grounded examples.
    path_sga2deg: contrain positive (un)grounded positive examples.
    path_out: output file contains grounded positive examples.
    is_train: if it is training set.
    path_label: if it is training set, we compress the isDEG corpus.
    '''
    # all the grounded examples.
    sga2deg_all = readsolution(path_solution)
    # positive examples.
    sga2deg = readsga2deg(path_sga2deg)
    # positive grounded examples.
    sga2deg = sga2deg.intersection(sga2deg_all)

    deg_corpus = set()
    for pair in sga2deg:
        deg_corpus.add(pair[1])

    if is_train:
        print 'saving to {}...'.format(path_label)
        f = open(path_label,'w')
        for gene in deg_corpus:
            print >> f, 'isDEG\t'+gene
        f.close

    sga2deg_list = dd(list)
    for line in sga2deg:
        sga = line[0]
        deg = line[1]
        sga2deg_list[sga].append(deg)

    path_all = dest+'/pathway_ground/tmp'
    print 'saving to {}...'.format(path_all)
    with io.open(path_all,'w') as file:
        for _, sga in enumerate(sga2deg_list):
            deg = sga2deg_list[sga]
            file.write(u'pathTo(%s,Y)'%sga)
            # TODO:
            for gene in deg_corpus:
                # TODO:
                if gene in deg:
                    file.write(u'\t+')
                else:
                    file.write(u'\t-')
                file.write(u'pathTo(%s,%s)'%(sga,gene))
            file.write(u'\n')

    examples = []
    for line in open(path_all, 'r'):
        line = line.strip()
        examples.append(line)

    print 'len(samples) = {}'.format(len(examples))

    SEED = 123
    random.seed(SEED)
    random.shuffle(examples)

    os.remove(path_all)

    save2txt_list(path_out,examples)
    return deg_corpus,sga2deg,set(sga2deg_list.keys())


if __name__ == '__main__':
    dest = '../pathway_forw_patient'
    deg_corpus_train,sga2deg_train,sga_corpus_train = extract_ground_in(dest+'/pathway_origin/train.solutions.txt', \
        dest+'/pathway_origin/sga2deg_train', dest+'/pathway_ground/train.examples', True, \
        dest+'/pathway_ground/labels.cfacts')

    deg_corpus_test,sga2deg_test,sga_corpus_test = extract_ground_in(dest+'/pathway_origin/test.solutions.txt', \
        dest+'/pathway_origin/sga2deg_test', dest+'/pathway_ground/test.examples', False)
    deg_corpus_remain,sga2deg_remain,sga_corpus_remain = extract_ground_in(dest+'/pathway_origin/remain.solutions.txt', \
        dest+'/pathway_origin/sga2deg_remain', dest+'/pathway_ground/remain.examples', False)

    print '_'*30
    print 'size of deg corpus:'
    print 'train\ttest\tremain'
    print '{}\t{}\t{}'.format(len(deg_corpus_train),len(deg_corpus_test),len(deg_corpus_remain))
    print 'train&test\ttrain&remain'
    print '{}\t{}'.format(len(deg_corpus_train.intersection(deg_corpus_test)), \
        len(deg_corpus_train.intersection(deg_corpus_remain)))

    print '_'*30
    print 'size of sga2deg:'
    print 'train\ttest\tremain'
    print '{}\t{}\t{}'.format(len(sga2deg_train),len(sga2deg_test),len(sga2deg_remain))
    print 'train&test\ttrain&remain'
    print '{}\t{}'.format(len(sga2deg_train.intersection(sga2deg_test)), \
        len(sga2deg_train.intersection(sga2deg_remain)))

    print '_'*30
    print 'size of sga corpus:'
    print 'train\ttest\tremain'
    print '{}\t{}\t{}'.format(len(sga_corpus_train),len(sga_corpus_test),len(sga_corpus_remain))
    print 'train&test\ttrain&remain'
    print '{}\t{}'.format(len(sga_corpus_train.intersection(sga_corpus_test)), \
        len(sga_corpus_train.intersection(sga_corpus_remain)))


    print 'Done!'
    # Q.E.D.