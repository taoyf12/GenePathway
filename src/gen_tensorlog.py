# Prepare date from raw data.
# prepare_forw_patient.py: separate the train, test dataset, and produce graph
# in a patient-wise manner.
from collections import defaultdict as dd
import io
import os
import random

# devide the data in the form of test, train and network.

# 2016/08/28
# especially for the patient-wised division of data.
# prepare the data for our experiments.

def get_sga2deg(path_sga2deg_all, path_sga2deg_train, patid_train):
    print 'reading from: {}...'.format(path_sga2deg_all)
    sga2deg = dd(float)
    sga2deg_str = []
    sga2deg_all_list = set()
    sga_corpus = set()
    deg_corpus = set()
    for line in open(path_sga2deg_all, 'r'):
        values = line.strip().split('\t')
        patid,sga,deg,prob = int(values[0]),values[1],values[2],float(values[3])
        sga2deg_all_list.add((sga,deg))
        if patid not in patid_train: continue
        sga2deg[(sga,deg)]+= prob
        sga_corpus.add(sga)
        deg_corpus.add(deg)
        #sga2deg_str.append('\t'.join(values))

    for row in sga2deg.keys():
        sga2deg_str.append('leadTo'+'\t'+row[0]+'\t'+row[1]+'\t'+str(sga2deg[row]))

    print 'saving to {}...'.format(path_sga2deg_train)
    f = open(path_sga2deg_train,'w')
    for row in sga2deg_str:
        print >> f, row
    f.close

    sga2deg = sga2deg.keys()
    return sga2deg,sga_corpus,deg_corpus,sga2deg_all_list

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
    
def writeSample(path, filename, sga2deglist, deg_corpus):
    # print 'saving to {}...'.format(path+'/'+filename)
    #i,j = 0,0
    with io.open(path+'/tmp','w') as file:
        for itr, sga in enumerate(sga2deglist):
            if itr%1000 == 0:
                print itr
            deg = sga2deglist[sga]
            file.write(u'pathTo(%s,Y)'%sga)
            # TODO:
            for gene in deg_corpus:
                # TODO:
                if gene in deg:
                    file.write(u'\t+')
                    #i += 1
                else:
                    file.write(u'\t-')
                    #j += 1
                file.write(u'pathTo(%s,%s)'%(sga,gene))
            file.write(u'\n')

    #print 'len(pos) = {}, len(neg) = {}'.format(i,j)

    examples = []
    for line in open(path+'/tmp', 'r'):
        line = line.strip()
        examples.append(line)

    print 'len(samples) = {}'.format(len(examples))

    SEED = 666
    random.seed(SEED)
    random.shuffle(examples)
    os.remove(path+'/tmp');
    path_out = path+'/'+filename
    save2txt_list(path_out,examples)


if __name__ == '__main__':

    #print 'preparing training and test set...'

    root = '/usr1/public/yifeng/GenePathway'
    dest = root+'/pathway_forw_patient'

    path_train = dest+'/pathway_origin/train'

    train_list = dd(list)
    for line in open(path_train, 'r'):
        values = line.strip().split('\t')
        sga,deg,prob = values[0],values[1],values[2]
        train_list[sga].append(deg)

    path_train_out = dest+'/pathway_origin/train.exam'


    with io.open(path_train_out,'w') as file:
        for itr, sga in enumerate(train_list):
            # if itr%1000 == 0:
            #     print itr
            deg = train_list[sga]
            file.write(u'pathTo')
            file.write(u'\t%s'%sga)
            # TODO:
            for gene in deg:
                file.write(u'\t%s'%gene)
            file.write(u'\n')




    path_test = dest+'/pathway_origin/test'

    test_list = dd(list)
    for line in open(path_test, 'r'):
        values = line.strip().split('\t')
        sga,deg,prob = values[0],values[1],values[2]
        test_list[sga].append(deg)

    path_test_out = dest+'/pathway_origin/test.exam'


    with io.open(path_test_out,'w') as file:
        for itr, sga in enumerate(test_list):
            # if itr%1000 == 0:
            #     print itr
            deg = test_list[sga]
            file.write(u'pathTo')
            file.write(u'\t%s'%sga)
            # TODO:
            for gene in deg:
                file.write(u'\t%s'%gene)
            file.write(u'\n')



    # deg_corpus_train = set()
    # path_deg_corpus_train = dest+'/pathway_origin/labels.cfacts'
    # print 'reading from: {}...'.format(path_deg_corpus_train)
    # for line in open(path_deg_corpus_train, 'r'):
    #     values = line.strip().split('\t')
    #     deg_corpus_train.add(values[1])

    # # path_train_example = dest+'/pathway_origin/train.examples'


    # sga2deglist_train = dd(list)
    # path_train = dest+'/pathway_origin/train'
    # print 'reading from: {}...'.format(path_train)
    # for line in open(path_train, 'r'):
    #     values = line.strip().split('\t')
    #     sga,deg,prob = values[0],values[1],float(values[2])
    #     sga2deglist_train[sga].append(deg)
    #     # sga2deg_all_list.add((sga,deg))

    # writeSample(dest+'/pathway_origin', 'train.examples', sga2deglist_train, deg_corpus_train)

    # # generate the testing set.


    # deg_corpus_test = set()
    # path_deg_corpus_test = dest+'/pathway_origin/labels.cfacts'

    # sga2deglist_test = dd(list)
    # path_test= dest+'/pathway_origin/test'
    # print 'reading from: {}...'.format(path_test)
    # for line in open(path_test, 'r'):
    #     values = line.strip().split('\t')
    #     sga,deg,prob = values[0],values[1],float(values[2])
    #     sga2deglist_test[sga].append(deg)
    #     deg_corpus_test.add(deg)
    #     # sga2deg_all_list.add((sga,deg))

    # writeSample(dest+'/pathway_origin', 'test.examples', sga2deglist_test, deg_corpus_test)

    # # 



    print 'Done!'
# Q.E.D.
