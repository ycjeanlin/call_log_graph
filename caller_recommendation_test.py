import cPickle
import operator
import codecs


def load_graph(filename):
    with open(filename, 'rb') as fp:
        graph = cPickle.load(fp)
    return graph


def recommend_users(caller, graph, max_degree, step, popularity):
    user_list = {}
    nodes = set()
    nodes.add(caller)

    while step > 1:
        next_nodes = set()
        for node in nodes:
            neighbors = graph.neighbors(node)
            for n in neighbors:
                    next_nodes.add(n)

        # step update
        nodes = next_nodes
        step -= 1

    for node in nodes:
        neighbors = graph.neighbors(node)
        for n in neighbors:
            if graph.degree(n) < max_degree:
                if n in user_list:
                    user_list[n] += 1
                else:
                    user_list[n] = 1

    neighbors = graph.neighbors(caller)
    candidate_users = {}
    for user in user_list:
        if user_list[user] >= popularity and user not in neighbors:
            candidate_users[user] = user_list[user]

    sorted_users = sorted(candidate_users.items(), key=operator.itemgetter(1), reverse=True)
    user_ids = [x[0] for x in sorted_users]

    return user_ids


if __name__ == '__main__':
    input_file = 'test_list'
    output_file = 'recommend_list.dat'

    print 'Graph loading'
    call_log_graph = load_graph('output.model')

    print ''
    with codecs.open(input_file, 'r') as fr:
        tel_callers = [x.strip().split('\t')[0] for x in fr.readlines()]

    with codecs.open(output_file, 'w') as fw:
        index = 0
        for tel_caller in tel_callers:
            index += 1
            if (index % 10) == 0:
                print index

            recommended_users = recommend_users(tel_caller, call_log_graph, 10, 3, 10)

            fw.write(tel_caller + '\t' + '\t'.join(recommended_users) + '\n')
