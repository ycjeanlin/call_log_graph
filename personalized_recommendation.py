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
        print '===Step', step, '==='
        next_nodes = set()
        for node in nodes:
            neighbors = graph.neighbors(node)
            for n in neighbors:
                    next_nodes.add(n)

        # step update
        nodes = next_nodes
        step -= 1

    print '===Final Step==='
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
        #print user[0], user[1]
        user_ids.append(user[0])
    #user_ids = [x[0] for x in sorted_users]

    return user_ids


def cal_performance(called_list, user_list):
    true_positive = 0.0
    for user in user_list:
        if user in called_list:
            true_positive += 1
    print 'True Positive: ', true_positive
    p = true_positive / len(user_list)
    r = true_positive / len(called_list)

    return p, r

if __name__ == '__main__':

    print 'Graph loading'
    call_log_graph = load_graph('test.model')

    print 'Test data loading'
    tel_call_list = {}
    fr = codecs.open('test_tel_call_list', 'r')
    for row in fr:
        cols = row.strip().split('\t')
        tel_call_list[cols[0]] = []
        for i in range(1, len(cols)):
            tel_call_list[cols[0]].append(cols[i])

    query = ''
    print "Enter [node_id]"
    while query != 'exit':
        query = raw_input('Enter:')
        if query == 'exit':
            break

        recommended_users = recommend_users(query, call_log_graph, 100, 3, 1)
        precision, recall = cal_performance(tel_call_list[query], recommended_users)
        print 'Precision: ', precision
        print 'Recall: ', recall

    print 'End'
