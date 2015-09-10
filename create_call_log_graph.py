import networkx as nx
import codecs
import cPickle


def create_graph(tel_logs):
    graph = nx.Graph()

    with codecs.open(tel_logs, 'r') as fr:
        index = 0
        for row in fr:
            index += 1
            if (index % 100000) == 0:
                print index

            cols = row.strip().split()
            if cols[0] not in graph:
                graph.add_node(cols[0])

            if cols[1] not in graph:
                graph.add_node(cols[1])

            if not graph.has_edge(cols[0], cols[1]):
                graph.add_edge(cols[0], cols[1])

    return graph


def write_graph(filename, graph):
    with open(filename, 'wb') as fp:
        cPickle.dump(graph, fp)


if __name__ == '__main__':
    print 'Graph creating'
    input_file = './data/train.dat'
    call_log_graph = create_graph(input_file)

    print 'Graph storing'
    write_graph('output.model', call_log_graph)