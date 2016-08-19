# Refine the data: get the abbreviated graph.
from collections import defaultdict as dd
import io
import random

def readfeatures(path):

    print 'reading from: {}...'.format(path)
    leadTo = set()
    for line in open(path, 'r'):
        values = line.strip().split('\t')
        if ('id(' in values[0]) or ('db(' in values[0]): continue
        val = values[0][2:-1]
        #print val
        val = val.strip().split(',')
        #print val
        leadTo.add(('leadTo',val[0],val[1],'1.0000'))
        #print val
    #     val = values[-1][:-1]
    #     val = val[7:-1]
    #     val = val.split(',')
    #     sga2deg_all.add((val[0],val[1]))
    #     #print val
    # print 'len(sga2deg_all) = {}'.format(len(sga2deg_all))
    return leadTo

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

    # Extract (sga, deg) pairs from dumped .sql file.
    path_features = '../pathway_refine/train.grounded.features'
    pathway = readfeatures(path_features)

    path_pathway = '../pathway_refine/pathway.graph'
    save2txt(path_pathway, pathway)

    # path_sga2deg = '../pathway/sga2deg.examples'
    # sga2deg = readsga2deg(path_sga2deg)
    # sga2deg_out = set()
    # for pair in sga2deg_all:
    #     if pair in sga2deg:
    #         sga2deg_out.add(pair)
    # # postive ones
    # sga2deg = sga2deg_out
    # print 'len(sga2deg) = {}'.format(len(sga2deg))

    # deg_corpus = set()
    # for pair in sga2deg:
    #     deg_corpus.add(pair[1])

    # path_label = '../pathway_refine/labels.cfacts'
    # print 'saving to {}...'.format(path_label)
    # f = open(path_label,'w')
    # for gene in deg_corpus:
    #     print >> f, 'isDEG\t'+gene
    # f.close
    # print 'len(deg_corpus) = {}'.format(len(deg_corpus))



    # sga2deg_list = dd(list)
    # for line in sga2deg:
    #     sga = line[0]
    #     deg = line[1]
    #     sga2deg_list[sga].append(deg)

    # path_all = '../pathway_refine/examples'
    # print 'saving to {}...'.format(path_all)
    # with io.open(path_all,'w') as file:
    #     for _, sga in enumerate(sga2deg_list):
    #         deg = sga2deg_list[sga]
    #         file.write(u'pathTo(%s,Y)'%sga)
    #         # TODO:
    #         for gene in deg_corpus:
    #             # TODO:
    #             if gene in deg:
    #                 file.write(u'\t+')
    #             else:
    #                 file.write(u'\t-')
    #             file.write(u'pathTo(%s,%s)'%(sga,gene))
    #         file.write(u'\n')

    # examples = []
    # for line in open(path_all, 'r'):
    #     line = line.strip()
    #     examples.append(line)

    # print 'len(samples) = {}'.format(len(examples))

    # SEED = 123
    # random.seed(SEED)
    # random.shuffle(examples)

    # path_train = '../pathway_refine/train.examples'
    # save2txt_list(path_train,examples)



    # path_test = '../pathway/test.examples'
    




    print 'Done!'


