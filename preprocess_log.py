import codecs
import operator
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


def split_train_test(tel_call_list):

    print 'Splitting'
    fw_train = codecs.open('./data/train.dat', 'w')
    fw_test = codecs.open('./data/test.dat', 'w')
    with codecs.open(tel_call_list, 'r') as fr:
        for row in fr:
            cols = row.strip().split('\t')
            if len(cols) >= 4:
                training_index, testing_index = train_test_split(range(1, len(cols)), test_size=0.4, random_state=7)
                if len(training_index) > 0 and len(testing_index) > 0:
                    training_cols = [cols[i] for i in training_index]
                    testing_cols = [cols[i] for i in testing_index]

                    for col in training_cols:
                        fw_train.write(cols[0] + '\t' + col + '\n')

                    for col in testing_cols:
                        fw_test.write(cols[0] + '\t' + col + '\n')
    fw_test.close()
    fw_train.close()

def gen_tel_list(call_logs, output_file):
    tel_list = {}
    with codecs.open(call_logs, 'r') as fr:
        fw = codecs.open(output_file, 'w')
        for row in fr:
            cols = row.strip().split('\t')
            if cols[1] in tel_list:
                tel_list[cols[1]] += 1
            else:
                tel_list[cols[1]] = 1

        sorted_tels = sorted(tel_list.items(), key=operator.itemgetter(1), reverse=True)

        for caller in sorted_tels:
            fw.write(caller[0] + '\t' + str(caller[1]) + '\n')

        fw.close()

def gen_tel_call_list(call_log, output_file):
    with codecs.open(call_log, 'r') as fr:
        fw = codecs.open(output_file, 'w')
        tel_called_list = {}
        index = 0
        for row in fr:
            index += 1
            if (index % 100000) == 0:
                print index

            cols = row.strip().split()
            if cols[1] in tel_called_list:
                tel_called_list[cols[1]].append(cols[0])
            else:
                tel_called_list[cols[1]] = []
                tel_called_list[cols[1]].append(cols[0])

        for caller in tel_called_list:
            fw.write(caller + '\t' + '\t'.join(tel_called_list[caller]) + '\n')

        fw.close()

if __name__ == '__main__':
    #extract_tel_logs('../whoscall_data/call_201408_tw.csv')
    #num_log = find_effective_logs(0, './data/tel_log_tw.dat')
    #split_train_test('./data/tel_call_list_0.dat')
    #gen_tel_list('./data/train.dat', './data/train_tel_list.dat')
    gen_tel_call_list('./data/test.dat', './data/tel_call_list_test.dat')
