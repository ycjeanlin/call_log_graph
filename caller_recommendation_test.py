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
    user_ids = []
    for user in sorted_users:
        user_ids.append(user[0])

    return user_ids


def cal_performance(called_list, user_list):
    true_positive = 0.0
    p = 0.0
    r = 0.0
    for user in user_list:
        if user in called_list:
            true_positive += 1
    print 'True Positive: ', true_positive
    if len(user_list) > 0 and len(called_list) > 0:
        p = true_positive / len(user_list)
        r = true_positive / len(called_list)

    return p, r


if __name__ == '__main__':
    input_file = './data/tel_call_list_test.dat'
    input_model = './graph.model'
    exp_file = './performance.csv'

    print 'Graph loading'
    call_log_graph = load_graph(input_model)

    print 'Test data loading'
    tel_call_list = {}
    fr = codecs.open(input_file, 'r')
    for row in fr:
        cols = row.strip().split('\t')
        tel_call_list[cols[0]] = []
        for i in range(1, len(cols)):
            tel_call_list[cols[0]].append(cols[i])

    index = 0
    fw = codecs.open(exp_file, 'w')
    for caller in tel_call_list:
        index += 1
        if (index % 10) == 0:
            print index

        print 'Caller: ', caller
        recommended_users = recommend_users(caller, call_log_graph, 100, 3, 1)
        precision, recall = cal_performance(tel_call_list[caller], recommended_users)
        print 'Precision: ', precision
        print 'Recall: ', recall
        fw.write(caller + ',' + str(precision) + ',' + str(recall) + '\n')

    fw.close()

