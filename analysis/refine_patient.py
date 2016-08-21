# Refine the data.
from collections import defaultdict as dd
import io
import random

def readsolution(path):
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
    print 'reading from: {}...'.format(path)
    sga2deg = set()
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        sga2deg.add((values[0],values[1]))
    #print 'len = {}'.format(len(sga2deg))
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


if __name__ == '__main__':

    # Extract (sga, deg) pairs from dumped .sql file.
    path_solution = '../pathway_patient/train.solutions.txt'
    sga2deg_all = readsolution(path_solution)
    # must be: sga2deg_train.examples
    path_sga2deg = '../pathway_patient/sga2deg_train.examples'
    sga2deg = readsga2deg(path_sga2deg)
    sga2deg_out = set()
    for pair in sga2deg_all:
        if pair in sga2deg:
            sga2deg_out.add(pair)
    # postive ones
    sga2deg = sga2deg_out
    print 'len(sga2deg_train) = {}'.format(len(sga2deg))

    deg_corpus = set()
    for pair in sga2deg:
        deg_corpus.add(pair[1])

    path_label = '../pathway_refine_patient/labels.cfacts'
    print 'saving to {}...'.format(path_label)
    f = open(path_label,'w')
    for gene in deg_corpus:
        print >> f, 'isDEG\t'+gene
    f.close
    print 'len(deg_corpus_actual) = {}'.format(len(deg_corpus))



    sga2deg_list = dd(list)
    for line in sga2deg:
        sga = line[0]
        deg = line[1]
        sga2deg_list[sga].append(deg)

    path_all = '../pathway_refine_patient/examples_train'
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

    path_train = '../pathway_refine_patient/train.examples'
    save2txt_list(path_train,examples)





    # Test data
    path_solution = '../pathway_patient/test.solutions.txt'
    sga2deg_all = readsolution(path_solution)
    # must be: sga2deg_train.examples
    path_sga2deg = '../pathway_patient/sga2deg_test.examples'
    sga2deg = readsga2deg(path_sga2deg)
    sga2deg_out = set()
    for pair in sga2deg_all:
        if pair in sga2deg:
            sga2deg_out.add(pair)
    # postive ones
    sga2deg = sga2deg_out
    print 'len(sga2deg_test) = {}'.format(len(sga2deg))

    deg_corpus = set()
    for pair in sga2deg:
        deg_corpus.add(pair[1])

    # path_label = '../pathway_refine_patient/labels.cfacts'
    # print 'saving to {}...'.format(path_label)
    # f = open(path_label,'w')
    # for gene in deg_corpus:
    #     print >> f, 'isDEG\t'+gene
    # f.close
    print 'len(deg_corpus_of_test) = {}'.format(len(deg_corpus))



    sga2deg_list = dd(list)
    for line in sga2deg:
        sga = line[0]
        deg = line[1]
        sga2deg_list[sga].append(deg)

    path_all = '../pathway_refine_patient/examples_test'
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

    path_test = '../pathway_refine_patient/test.examples'
    save2txt_list(path_test,examples)
    






    # Test data
    path_solution = '../pathway_patient/remain.solutions.txt'
    sga2deg_all = readsolution(path_solution)
    # must be: sga2deg_train.examples
    path_sga2deg = '../pathway_patient/sga2deg_remain.examples'
    sga2deg = readsga2deg(path_sga2deg)
    sga2deg_out = set()
    for pair in sga2deg_all:
        if pair in sga2deg:
            sga2deg_out.add(pair)
    # postive ones
    sga2deg = sga2deg_out
    print 'len(sga2deg_remain) = {}'.format(len(sga2deg))

    deg_corpus = set()
    for pair in sga2deg:
        deg_corpus.add(pair[1])

    # path_label = '../pathway_refine_patient/labels.cfacts'
    # print 'saving to {}...'.format(path_label)
    # f = open(path_label,'w')
    # for gene in deg_corpus:
    #     print >> f, 'isDEG\t'+gene
    # f.close
    print 'len(deg_corpus_of_remain) = {}'.format(len(deg_corpus))



    sga2deg_list = dd(list)
    for line in sga2deg:
        sga = line[0]
        deg = line[1]
        sga2deg_list[sga].append(deg)

    path_all = '../pathway_refine_patient/examples_remain'
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

    path_remain = '../pathway_refine_patient/remain.examples'
    save2txt_list(path_remain,examples)











    print 'Done!'


