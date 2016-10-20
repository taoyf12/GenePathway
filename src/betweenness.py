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

    print 'calculating centrality...'

    root = '/usr1/public/yifeng/GenePathway'
    dest = root+'/pathway'

    path_sga2deg = dest+'/remain'

    # sga,deg,dist
    # sga2deg = list()
    sga_corpus = set()
    deg_corpus = set()
    sga2deg = dd(list)

    dist = dd(float)
    center = dd(str)

    print 'reading from: {}...'.format(path_sga2deg)

    for line in open(path_sga2deg, 'r'):
        values = line.strip().split('\t')
        sga_corpus.add(values[0])
        deg_corpus.add(values[1])
        sga2deg[values[0]].append([values[1],1.0/float(values[2])])
        #sga2deg.append([values[0],values[1],1.0/float(values[2])])
    # print sga2deg

    # shortpath = list()

    # 
    print 'counting shortest path...'
    i = 0
    for sga in sga_corpus:
        i += 1
        if i%1000 == 0:
            print i
        for vcom in sga2deg[sga]:
            v = vcom[0]
            d1 = vcom[1]
            #print vcom
            for degcom in sga2deg[v]:
                deg  =degcom[0]
                d2 = degcom[1]
                if dist[(sga,deg)] == 0:
                    dist[(sga,deg)] = 1000000000
                if (d1+d2) < dist[(sga,deg)]:
                    dist[(sga,deg)] = d1+d2
                    center[(sga,deg)] = v


    gv = dd(float)
    for k,v in center.iteritems():
        gv[v] += 1

    print 'counting betweeness...'

    path_betweenness = root+'/src/betweenness'
    f = open(path_betweenness, 'w')
    for v,val in gv.iteritems():
        print >> f, v+'\t'+str(val)

    f.close()
    # path_sga2deg_remain_pat = dest+'/remain_pat'
    # print 'saving to {}...'.format(path_sga2deg_remain_pat)
    # f = open(path_sga2deg_remain_pat, 'w')
    # for row in sga2deg_remain.keys():
    #     print >> f, row[0]+'\t'+row[1]+'\t'+str(1.0*sga2deg_remain[row]/num_sga[row[0]])
    # f.close()
    # # sga2deg,sga_corpus,deg_corpus,sga2deg_all_list = extract_sga2deg(path_sga2deg_all, path_sga2deg_train, patid_train)






    # #print 1.0*len(sga2deg)/1496128,1.0*len(sga_corpus)/9829,1.0*len(deg_corpus)/5776


    # path_graph = dest+'/pathway.graph'
    # print 'saving to {}...'.format(path_graph)
    # f = open(path_graph,'w')
    # for row in sga2deg_remain.keys():
    #     sga,deg,prob = row[0],row[1],str(sga2deg_remain[row])
    #     print >> f, 'leadTo\t'+sga+'\t'+deg+'\t'+prob

    # f.close

    # # the weight which is adjusted based on occurence in patients.
    # path_graph_imp = dest+'/pathway_imp.graph'
    # print 'saving to {}...'.format(path_graph_imp)
    # f = open(path_graph_imp,'w')
    # for row in sga2deg_remain.keys():
    #     # adjusted here.
    #     sga,deg,prob = row[0],row[1],str(1.0*sga2deg_remain[row]/num_sga[row[0]])
    #     print >> f, 'leadTo\t'+sga+'\t'+deg+'\t'+prob

    # f.close

    # # get the labels.cfacts
    # path_label = dest+'/labels.cfacts'
    # print 'saving to {}...'.format(path_label)
    # f = open(path_label,'w')
    # for deg in deg_train_corpus:
    #     print >> f, 'isDEG\t'+deg
    # f.close
    print 'Done!'
# Q.E.D.
