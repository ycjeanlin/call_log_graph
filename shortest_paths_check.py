import cPickle
import codecs
import networkx as nx


def load_graph(filename):
    with open(filename, 'rb') as fp:
        graph = cPickle.load(fp)
    return graph

if __name__ == '__main__':
    input_file = './data/tel_call_list_test.dat'
    input_model = './graph.model'
    #exp_file = './performance.csv'

    print 'Graph loading'
    call_log_graph = load_graph(input_model)

    print 'Test data loading'
    tel_call_list = {}
    with codecs.open(input_file, 'r') as fr:
        for row in fr:
            cols = row.strip().split('\t')
            tel_call_list[cols[0]] = []
            for i in range(1, len(cols)):
                tel_call_list[cols[0]].append(cols[i])

    with codecs.open('shortest_path.csv', 'w') as fw:
        index = 0
        for caller in tel_call_list:
            index += 1
            if (index % 1000) == 0:
                print index

            distance_count = {}
            fw.write(caller)
            for user in tel_call_list[caller]:
                distance = 0
                if user in call_log_graph and nx.has_path(call_log_graph, caller, user):
                    distance = nx.shortest_path_length(call_log_graph, caller, user)

                if distance in distance_count:
                    distance_count[distance] += 1
                else:
                    distance_count[distance] = 1
            for d in distance_count:
                fw.write(',' + str(d) + ':' + str(distance_count[d]))
            fw.write('\n')