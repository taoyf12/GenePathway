import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def draw_graph(graph, path_pdf):
    pp = PdfPages(path_pdf)
    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    G=nx.Graph()

    # add nodes
    for node in nodes:
        G.add_node(node)

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # draw graph
    pos = nx.shell_layout(G)
    nx.draw(G, pos)

    # show graph
    #plt.show()
    pp.savefig()
    pp.close()
# draw example


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
        if i % 1000 == 1:
            graph.append((genex,geney))
    print 'drawing network...'
    path_pdf = 'network.pdf'
    draw_graph(graph, path_pdf)
    print 'Done!'