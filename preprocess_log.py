import codecs
import operator
from sklearn.cross_validation import train_test_split


def extract_tel_logs(call_logs, output_file):
    print 'Extract telemarketing logs from original call logs'
    tel_set = set()
    with codecs.open('./data/telemarketing_list.dat', 'r') as fr:
        rows = fr.readlines()
        for row in rows:
            cols = row.strip().split('\t')
            tel_set.add(cols[0])

    with codecs.open(call_logs, 'r') as fr:
        fw = codecs.open(output_file, 'w')
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


def find_effective_logs(threshold, tel_logs, output_file):
    print 'Find effective logs which duration bigger than ', threshold
    with codecs.open(tel_logs, 'r') as fr:
        fw = codecs.open(output_file, 'w')
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


def split_train_test(tel_call_list, output_train, output_test, min_occur):
    print 'Splitting training data and testing data'
    fw_train = codecs.open(output_train, 'w')
    fw_test = codecs.open(output_test, 'w')
    with codecs.open(tel_call_list, 'r') as fr:
        for row in fr:
            cols = row.strip().split('\t')
            if len(cols) >= (min_occur + 1):
                training_index, testing_index = train_test_split(range(1, len(cols)), test_size=0.3, random_state=7)
                if len(training_index) > 0 and len(testing_index) > 0:
                    training_cols = [cols[i] for i in training_index]
                    testing_cols = [cols[i] for i in testing_index]

                    for col in training_cols:
                        fw_train.write(col + '\t' + cols[0]  + '\n')

                    for col in testing_cols:
                        fw_test.write(col + '\t' + cols[0] + '\n')
    fw_test.close()
    fw_train.close()


def gen_tel_call_list(call_log, output_file):
    print 'Generate telemarketing number call list', call_log
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
                tel_called_list[cols[1]].add(cols[0])
            else:
                tel_called_list[cols[1]] = set()
                tel_called_list[cols[1]].add(cols[0])

        for caller in tel_called_list:
            fw.write(caller + '\t' + '\t'.join(tel_called_list[caller]) + '\n')

        fw.close()

if __name__ == '__main__':
    #extract_tel_logs('../whoscall_data/call_201408_tw.csv', './data/tel_log_tw.dat')
    #find_effective_logs(0, './data/tel_log_tw.dat', './data/tel_log_0.dat')
    gen_tel_call_list('./data/tel_log_0.dat', './data/tel_call_list_0.dat')
    #split_train_test('./data/tel_call_list_0.dat', './data/train.dat', './data/test.dat', 6)
    gen_tel_call_list('./data/test.dat', './data/tel_call_list_test.dat')
