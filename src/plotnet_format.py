import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=16, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif',
               path_pdf = 'network.pdf'):

    pp = PdfPages(path_pdf)
    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # these are different layouts for the network you may try
    # shell seems to work best
    print 'calculating position...'
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    elif graph_layout == 'graphviz':
        graph_pos=nx.graphviz_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    print 'plotting network...'
    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    #nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
    #                        font_family=text_font)

    #if labels is None:
    #    labels = range(len(graph))

    #edge_labels = dict(zip(graph, labels))
    #nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, 
    #                             label_pos=edge_text_pos)

    # show graph
    #plt.show()
    pp.savefig()
    pp.close()

if __name__ == '__main__':

    graph = []
    # [(20, 21),(21, 22),(22, 23), (23, 24),(24, 25), (25, 20), (20, 20)]
    path_graph = '../pathway/pathway.graph'
    print 'reading from: {}...'.format(path_graph)
    i = 0
    for line in open(path_graph, 'r'):
        i += 1
        values = line.strip().split('\t')
        genex = values[1].lower()
        geney = values[2].lower()
        #print genex, geney
        if i % 500 == 1:
            print 'proceed: {}%'.format(100.0*i/155900)
            graph.append((genex,geney))
    print 'drawing network...'
    path_pdf = 'network.pdf'
    #node_size = 100
    #draw_graph(graph, path_pdf,node_size)
    

    # you may name your edge labels
    #labels = map(chr, range(65, 65+len(graph)))
    #draw_graph(graph, labels)

    # if edge labels is not specified, numeric labels (0, 1, 2...) will be used
    draw_graph(graph,graph_layout='spring',path_pdf = path_pdf)
    print 'Done!'