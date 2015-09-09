import codecs


def extract_tel_logs(call_logs):
    tel_set = set()
    with codecs.open('telemarketing_list.dat', 'r') as fr:
        rows = fr.readlines()
        for row in rows:
            cols = row.strip().split('\t')
            tel_set.add(cols[0])

    with codecs.open(call_logs, 'r') as fr:
        fw = codecs.open('tel_log_tw.dat', 'w')
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
        fw = codecs.open('tel_log_0.dat', 'w')
        index = 0
        for row in fr:
            index += 1
            if (index % 100000) == 0:
                print index

            cols = row.strip().split('\t')
            duration = int(cols[4])
            if duration > threshold:
                fw.write(cols[1] + '\t' + cols[2] + '\t' + cols[3]+ '\t' + cols[4] + '\n')

        print 'Line Number: ', index
        fw.close()


if __name__ == '__main__':
    #extract_tel_logs('../whoscall_data/call_201408_tw.csv')
    find_effective_logs(0, 'tel_log_tw.dat')
