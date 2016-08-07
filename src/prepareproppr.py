# prepare the files required by ProPPR.
from collections import defaultdict as dd
import io

def save2txt(path, table):
    print 'saving to {}...'.format(path)
    f = open(path, 'w')
    for row in table:
        print >> f, '\t'.join(row)
    f.close()

# TODO: add edges to node itself
if __name__ == '__main__':

    path_pathway = '../TDI_dump/pathway.cfacts'
    print 'reading from: {}...'.format(path_pathway)
    path_pathway_out = '../pathway/pathway.graph'
    f = open(path_pathway_out, 'w')
    print 'saving to: {}...'.format(path_pathway_out)

    corpus = set()
    for line in open(path_pathway, 'r'):
        values = line.strip().split('\t')
        genex = values[1].lower()
        geney = values[2].lower()
        #genex = values[1]
        #geney = values[2]
        corpus.add(genex)
        corpus.add(geney)
        print >> f, 'leadTo\t{}\t{}\t1.0000'.format(genex,geney)

    f.close()
    print 'nodes = {}'.format(len(corpus))


    path_sga2deg = '../TDI_dump/sga2deg_large.txt'
    print 'reading from: {}...'.format(path_sga2deg)
    path_sga2deg_out = '../TDI_dump/sga2deg.txt'
    # sgaid2degid = readTDI(path_tdi,2,4)
    sga2deg = set()
    for line in open(path_sga2deg, 'r'):
        values = line.strip().split('\t')
        #print values
        genex = values[0].lower()
        geney = values[1].lower()
        if (genex in corpus) and (geney in corpus):
            sga2deg.add((genex,geney))

    print 'sorting...'
    sga2deg = sorted(sga2deg, key = lambda item:(item[0],item[1]))
    print 'len = {}'.format(len(sga2deg))
    save2txt(path_sga2deg_out,sga2deg)

    sga2deg_list = dd(list)
    for line in sga2deg:
        sga = line[0]
        deg = line[1]
        sga2deg_list[sga].append(deg)

    path_train = '../pathway/examples'
    print 'generating {}...'.format(path_train)
    with io.open(path_train,'w') as file:
        for _, sga in enumerate(sga2deg_list):
            deg = sga2deg_list[sga]
            file.write(u'pathTo(%s,Y)'%sga)
            for gene in corpus:
                if (gene in deg) or (gene == sga):
                    file.write(u'\t+')
                else:
                    file.write(u'\t-')
                file.write(u'pathTo(%s,%s)'%(sga,gene))
            file.write(u'\n')




