import cPickle
import operator
import codecs
import networkx as nx


def load_graph(filename):
    with open(filename, 'rb') as fp:
        graph = cPickle.load(fp)
    return graph


def recommend_users(caller, graph, max_degree, step):
    users_list = {}
    nodes = set(caller)

    while step > 1:
        next_nodes = set()
        for node in nodes:
            neighbors = graph.neighbors(node)
            for n in neighbors:
                if graph.degree(n) < max_degree and graph.degree(n) > 1:
                     next_nodes.add(n)

        # step update
        nodes = next_nodes
        step -= 1

    for node in nodes:
        neighbors = graph.neighbors(node)
        for n in neighbors:
            if graph.degree(n) < max_degree and graph.degree(n) > 1:
                next_nodes.add(n)
                if n in users_list:
                     users_list[n] += 1
                else:
                    users_list[n] = 1
    neighbors = graph.neighbors(caller)
    for user in users_list:
        if users_list[user] < 5 or user in neighbors:
            users_list.pop(user)

    sorted_users = sorted(users_list.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_users


if __name__ == '__main__':
    print 'Graph loading'
    call_log_graph = load_graph('output.model')

    print ''
    with codecs.open('./data/train_tel_list.dat', 'r') as fr:
        tel_callers = fr.readlines()

    with codecs.open('recommend_list.dat', 'w') as fw:
        index = 0
        for tel_caller in tel_callers:
            print tel_caller
            index += 1
            if (index % 1000) == 0:
                print index

            recommended_users = recommend_users(tel_caller, call_log_graph, 2, 3).keys()

            fw.write(tel_caller + '\t' + '\t'.join(recommended_users) + '\n')
