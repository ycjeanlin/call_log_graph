import codecs
from sklearn.cross_validation import train_test_split


def extract_tel_logs(call_logs):
    tel_set = set()
    with codecs.open('./data/telemarketing_list.dat', 'r') as fr:
        rows = fr.readlines()
        for row in rows:
            cols = row.strip().split('\t')
            tel_set.add(cols[0])

    with codecs.open(call_logs, 'r') as fr:
        fw = codecs.open('./data/tel_log_tw.dat', 'w')
        index = 0
        for row in fr:
            index += 1
            if (index % 1000000) == 0:
                print index

            if len(row) > 1:  # skip the blank rows
                col = [x.strip('"') for x in row.strip().split(',')]
                if col[2] in tel_set:
                    fw.write('\t'.join(col) + '\n')
        fw.close()


def find_effective_logs(threshold, tel_logs):
    with codecs.open(tel_logs, 'r') as fr:
        fw = codecs.open('./data/tel_log_0.dat', 'w')
        index = 0
        size = 0
        for row in fr:
            index += 1
            if (index % 100000) == 0:
                print index

            cols = row.strip().split('\t')
            duration = int(cols[4])
            if duration > threshold:
                size += 1
                fw.write(cols[1] + '\t' + cols[2] + '\t' + cols[3] + '\t' + cols[4] + '\n')

        print 'Line Number: ', size
        fw.close()
        return size


def split_train_test(total_size):
    print 'Sampling'
    training_index, testing_index = train_test_split(range(total_size), test_size=0.30, random_state=13)

    print 'Splitting'
    with codecs.open('./data/tel_log_0.dat', 'r') as fr:
        rows = fr.readlines()
        training_rows = [rows[i] for i in training_index]
        testing_rows = [rows[i] for i in testing_index]

    print 'Training data output'
    with codecs.open('./data/train.dat', 'w') as fw:
        for row in training_rows:
            fw.write(row)

    print 'Testing data output'
    with codecs.open('./data/test.dat', 'w') as fw:
        for row in testing_rows:
            fw.write(row)


if __name__ == '__main__':
    #extract_tel_logs('../whoscall_data/call_201408_tw.csv')
    num_log = find_effective_logs(0, './data/tel_log_tw.dat')
    split_train_test(num_log)
