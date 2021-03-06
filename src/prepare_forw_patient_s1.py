# generate in the way of weight(SGA -> DEG) = \sum (posterior prob) / Number_of_tumors_with_SGA
from collections import defaultdict as dd
import io
import os
import random


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

    print 'preparing training and test set...'

    root = '/usr1/public/yifeng/GenePathway'
    dest = root+'/pathway'


    # get the training(?) edgesself.

    NUM_PAT = 4468
    patid_list = range(1,NUM_PAT+1)
    SEED = 888
    random.seed(SEED)
    random.shuffle(patid_list)

    thresh1 = 0.1
    thresh2 = 0.2
    cut1 = int(thresh1*NUM_PAT)
    cut2 = int(thresh2*NUM_PAT)
    patid_train = patid_list[0:cut1]
    patid_test = patid_list[cut1:cut2]
    patid_remain = patid_list[cut2:]

    # check
    print len(patid_train),len(patid_test),len(patid_remain),len(patid_train)+len(patid_test)+len(patid_remain)

    path_sga2deg_all = dest+'/pathway_processed/pathway_pat_all.graph'
    path_sga2deg_train = dest+'/train'
    path_sga2deg_test = dest+'/test'
    path_sga2deg_remain = dest+'/remain'


    print 'reading from: {}...'.format(path_sga2deg_all)

    sga2deg_train = dd(float)
    sga2deg_test = dd(float)
    sga2deg_remain = dd(float)

    sga2deg_remain_imp = dd(float)

    sga_train_corpus = set()
    deg_train_corpus = set()
    sga_test_corpus = set()
    deg_test_corpus = set()
    sga_remain_corpus = set()
    deg_remain_corpus = set()

    count = 0

    sga2pat = dd(set)
    num_sga = dd(int)

    for line in open(path_sga2deg_all, 'r'):
        count += 1
        if count%1000000 == 0:
            print count
        values = line.strip().split('\t')
        patid,sga,deg,prob = int(values[0]),values[1],values[2],float(values[3])
        if patid in patid_train:
            sga_train_corpus.add(sga)
            deg_train_corpus.add(deg)
            sga2deg_train[(sga,deg)] += prob
        elif patid in patid_test:
            sga_test_corpus.add(sga)
            deg_test_corpus.add(deg)
            sga2deg_test[(sga,deg)] += prob
        elif patid in patid_remain:
            sga_remain_corpus.add(sga)
            deg_remain_corpus.add(deg)
            sga2deg_remain[(sga,deg)] += prob

            sga2pat[sga].add(patid)
        else:
            print 'error!!!'

    for k in sga2pat:
        num_sga[k] = len(sga2pat[k])

    print 'saving to {}...'.format(path_sga2deg_train)
    f = open(path_sga2deg_train, 'w')
    for row in sga2deg_train.keys():
        print >> f, row[0]+'\t'+row[1]+'\t'+str(sga2deg_train[row])
    f.close()

    print 'saving to {}...'.format(path_sga2deg_test)
    f = open(path_sga2deg_test, 'w')
    for row in sga2deg_test.keys():
        print >> f, row[0]+'\t'+row[1]+'\t'+str(sga2deg_test[row])
    f.close()

    print 'saving to {}...'.format(path_sga2deg_remain)
    f = open(path_sga2deg_remain, 'w')
    for row in sga2deg_remain.keys():
        print >> f, row[0]+'\t'+row[1]+'\t'+str(sga2deg_remain[row])
    f.close()


    path_sga2deg_remain_pat = dest+'/remain_pat'
    print 'saving to {}...'.format(path_sga2deg_remain_pat)
    f = open(path_sga2deg_remain_pat, 'w')
    for row in sga2deg_remain.keys():
        print >> f, row[0]+'\t'+row[1]+'\t'+str(1.0*sga2deg_remain[row]/num_sga[row[0]])
    f.close()
    # sga2deg,sga_corpus,deg_corpus,sga2deg_all_list = extract_sga2deg(path_sga2deg_all, path_sga2deg_train, patid_train)


    print 'sga2deg_train\tsga2deg_test\tsga2deg_remain'
    print '{}\t\t{}\t\t{}'.format(len(sga2deg_train.keys()),len(sga2deg_test.keys()),len(sga2deg_remain.keys()))
    print '\t\t{}\t\t{}'.format(len(set(sga2deg_train.keys()).intersection(set(sga2deg_test.keys()))), \
        len(set(sga2deg_train.keys()).intersection(set(sga2deg_remain.keys()))))

    print 'sga_train\tsga_test\tsga_remain'
    print '{}\t\t{}\t\t{}'.format(len(sga_train_corpus),len(sga_test_corpus),len(sga_remain_corpus))
    print '\t\t{}\t\t{}'.format(len(sga_train_corpus.intersection(sga_test_corpus)), \
        len(sga_train_corpus.intersection(sga_remain_corpus)))

    print 'deg_train\tdeg_test\tdeg_remain'
    print '{}\t\t{}\t\t{}'.format(len(deg_train_corpus),len(deg_test_corpus),len(deg_remain_corpus))
    print '\t\t{}\t\t{}'.format(len(deg_train_corpus.intersection(deg_test_corpus)), \
        len(deg_train_corpus.intersection(deg_remain_corpus)))



    #print 1.0*len(sga2deg)/1496128,1.0*len(sga_corpus)/9829,1.0*len(deg_corpus)/5776


    path_graph = dest+'/pathway.graph'
    print 'saving to {}...'.format(path_graph)
    f = open(path_graph,'w')
    for row in sga2deg_remain.keys():
        sga,deg,prob = row[0],row[1],str(sga2deg_remain[row])
        print >> f, 'leadTo\t'+sga+'\t'+deg+'\t'+prob

    f.close

    # the weight which is adjusted based on occurence in patients.
    path_graph_imp = dest+'/pathway_imp.graph'
    print 'saving to {}...'.format(path_graph_imp)
    f = open(path_graph_imp,'w')
    for row in sga2deg_remain.keys():
        # adjusted here.
        sga,deg,prob = row[0],row[1],str(1.0*sga2deg_remain[row]/num_sga[row[0]])
        print >> f, 'leadTo\t'+sga+'\t'+deg+'\t'+prob

    f.close

    # get the labels.cfacts
    path_label = dest+'/labels.cfacts'
    print 'saving to {}...'.format(path_label)
    f = open(path_label,'w')
    for deg in deg_train_corpus:
        print >> f, 'isDEG\t'+deg
    f.close
    print 'Done!'
# Q.E.D.
