# Generate the final data to be read by Tensorlog.
from collections import defaultdict as dd
import io
import os
import random

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
    dest = root+'/TensorLog-dev/src/pathway'

    geneset = set()

    path_graph = dest+'/pathway.graph'
    graph = []
    for line in open(path_graph, 'r'):
        values = line.strip()
        graph.append(values)
        lt = values.split('\t')
        geneset.add(lt[1])
        geneset.add(lt[2])
        #print lt[1],lt[2]
    #print len(geneset)

    path_label = dest+'/labels.cfacts'
    label = []
    for line in open(path_label, 'r'):
        values = line.strip()
        label.append(values)

    path_train = dest+'/train'
    train = []
    for line in open(path_train, 'r'):
        values = line.strip().split('\t')
        train.append(values[:-1])
        geneset.add(values[0])
        geneset.add(values[1])

    #print train
    path_test = dest+'/test'
    test = []
    for line in open(path_test, 'r'):
        values = line.strip().split('\t')
        test.append(values[:-1])
        geneset.add(values[0])
        geneset.add(values[1])

    print len(geneset)

    path_cfacts = dest+'/pathway.cfacts'

    print 'saving to {}...'.format(path_cfacts)
    f = open(path_cfacts, 'w')
    for row in graph:
        print >> f, row
    print >> f, ''
    for row in label:
        print >> f, row
    print >> f, ''
    for row in train:
        print >> f, 'train\t'+'\t'.join(row)
    print >> f, ''
    for row in test:
        print >> f, 'test\t'+'\t'.join(row)
    print >> f, ''
    print >> f, 'rule\tf1'
    print >> f, 'rule\tf2'

    print >> f, ''
    for gene in geneset:
        print >> f, 'src\t'+gene
    print >> f, ''
    for gene in geneset:
        print >> f, 'dst\t'+gene

    f.close()
    print 'Done!'
# Q.E.D.
