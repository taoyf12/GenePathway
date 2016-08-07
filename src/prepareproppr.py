# prepare the files required by ProPPR.

# def readTDI(path, pos_sga, pos_deg):
#     '''
#     This readTDI function simply deduplicate all the 
#     (sga, deg) pairs.
#     '''
#     print 'reading from: {}...'.format(path)
#     sga2deg = set()
#     i = 0
#     for line in open(path, 'r'):
#         i += 1
#         values = line.split('),(')
#         if 'INSERT INTO' in values[0]:
#             values[-1] = values[-1][:-3]
#             tmp = values[0].split('(')
#             values[0] = tmp[1]
#             for val in values:
#                 row = val.split(',')
#                 if row[pos_sga] != 'NULL':
#                     sga2deg.add((row[pos_sga],row[pos_deg]))
#     sga2deg = list(sga2deg)
#     print 'sorting...'
#     sga2deg = sorted(sga2deg, key = lambda item:(int(item[0]),int(item[1])))
#     print 'len = {}'.format(len(sga2deg))
#     return sga2deg

# def readSQL(path, pos_src, pos_dist):
#     print 'reading from: {}...'.format(path)
#     src2dist = {}
#     i = 0
#     for line in open(path, 'r'):
#         i += 1
#         values = line.split('),(')
#         if 'INSERT INTO' in values[0]:
#             # modify first and last string in list.
#             values[-1] = values[-1][:-3]
#             tmp = values[0].split('(')
#             values[0] = tmp[1]
#             # val: 45009,181,3437,NULL,'TCGA-13-0751','CDH11'
#             for val in values:
#                 row = val.split(',')
#                 # TODO: row[2] can be NULL...?
#                 src2dist[row[pos_src]] = row[pos_dist]

#     print 'len = {}'.format(len(src2dist))
#     return src2dist

def save2txt(path, table):
    print 'saving to {}...'.format(path)
    f = open(path, 'w')
    for row in table:
        print >> f, '\t'.join(row)
    f.close()

if __name__ == '__main__':

    path_pathway = '../TDI_dump/pathway.cfacts'
    print 'reading from: {}...'.format(path_pathway)
    path_pathway_out = '../pathway/pathway.graph'
    f = open(path_pathway_out, 'w')
    
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

        # for val in values:
        #     print val
    #         row = val.split(',')
    #         if row[pos_sga] != 'NULL':
    #             sga2deg.add((row[pos_sga],row[pos_deg]))
    # sga2deg = list(sga2deg)
    print 'sorting...'
    sga2deg = sorted(sga2deg, key = lambda item:(item[0],item[1]))
    print 'len = {}'.format(len(sga2deg))
    save2txt(path_sga2deg_out,sga2deg)
    # return sga2deg





    # # sga_id to gen_id
    # path_sga = '../TDI_dump/SGAs.sql'
    # sgaid2genid = readSQL(path_sga,0,2)

    # path_deg = '../TDI_dump/DEGs.sql'
    # degid2genid = readSQL(path_deg,0,2)

    # path_gen = '../TDI_dump/Genes.sql'
    # genid2gen = readSQL(path_gen,0,1)

    # sga2deg = set()
    # for row in sgaid2degid:
    #     sga_tmp = sgaid2genid[row[0]]
    #     deg_tmp = degid2genid[row[1]]
    #     #print row[0], sga_tmp
    #     if sga_tmp == 'NULL':
    #         continue
    #     else:
    #         sga = genid2gen[sga_tmp]
    #         deg = genid2gen[deg_tmp]
    #         # TODO: lowever case?
    #         # remove ''
    #         sga2deg.add((sga[1:-1],deg[1:-1]))
    # sga2deg = list(sga2deg)
    # print 'sorting...'
    # sga2deg = sorted(sga2deg, key = lambda item:(item[0], item[1]))

    # path_sga2deg = '../TDI_dump/sga2deg_large.txt'
    # save2txt(path_sga2deg, sga2deg)