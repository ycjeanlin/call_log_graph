import cPickle
import operator
import codecs


def load_graph(filename):
    with open(filename, 'rb') as fp:
        graph = cPickle.load(fp)
    return graph

def recommend_users_similarity(graph, main_caller, min_similarity, topk):

    caller_neighbors = graph.neighbors(main_caller)
    num_neighbors = len(caller_neighbors)
    caller_paths = {}
    for user in caller_neighbors:
        for n in graph.neighbors(user):
            if n in caller_paths:
                caller_paths[n] += 1
            else:
                caller_paths[n] = 1

    referrers = {}
    for caller in caller_paths:
        if caller_paths[caller] / float(num_neighbors) >= min_similarity:
            referrers[caller] = caller_paths[caller]

    user_paths = {}
    for referrer in referrers:
        if referrer != main_caller:
            users = graph.neighbors(referrer)
            num_paths = referrers[referrer]
            for user in users:
                if user not in caller_neighbors:
                    if user in user_paths:
                        user_paths[user] += num_paths
                    else:
                        user_paths[user] = num_paths

    sorted_users = sorted(user_paths.items(), key=operator.itemgetter(1), reverse=True)

    candidate_users = []
    i = 0
    num_users = len(sorted_users)
    while i < num_users and i < topk:
        candidate_users.append(sorted_users[i][0])
        i += 1

    return candidate_users


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
    tp = 0.0
    p = 0.0
    r = 0.0
    for user in user_list:
        if user in called_list:
            tp += 1

    if len(user_list) > 0 and len(called_list) > 0:
        p = tp / len(user_list)
        r = tp / len(called_list)

    return tp, p, r


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

        #print 'Caller: ', caller
        #recommended_users = recommend_users(caller, call_log_graph, 200, 3, 1)
        recommended_users = recommend_users_similarity(call_log_graph, caller, 0.3, 100)
        true_positive, precision, recall = cal_performance(tel_call_list[caller], recommended_users)
        #print 'Precision: ', precision
        #print 'Recall: ', recall
        fw.write(caller + ',' + str(true_positive)+ ',' + str(precision) + '\n')

    fw.close()

