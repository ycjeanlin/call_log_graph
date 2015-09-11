import cPickle
import operator
import codecs


def load_graph(filename):
    with open(filename, 'rb') as fp:
        graph = cPickle.load(fp)
    return graph


def recommend_users(graph, main_caller, min_similarity, topk):

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
    print sorted_users
    candidate_users = []
    i = 0
    num_users = len(sorted_users)
    while i < num_users and i < topk:
        candidate_users.append(sorted_users[i][0])
        i += 1

    return candidate_users


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
    call_log_graph = load_graph('graph.model')

    print 'Test data loading'
    tel_call_list = {}
    with codecs.open('./data/tel_call_list_test.dat', 'r') as fr:
        for row in fr:
            cols = row.strip().split('\t')
            tel_call_list[cols[0]] = []
            for i in range(1, len(cols)):
                tel_call_list[cols[0]].append(cols[i])

    query = ''
    print 'Enter [node_id]'
    while query != 'exit':
        try:
            query = raw_input('Enter:')
            if query == 'exit':
                break
            tel_caller, similarity = query.split()

            recommended_users = recommend_users(call_log_graph, tel_caller, float(similarity), 10)

            precision, recall = cal_performance(tel_call_list[tel_caller], recommended_users)
            print 'Precision: ', precision
            #print 'Recall: ', recall
        except Exception, e:
            print str(e)

    print 'End'
