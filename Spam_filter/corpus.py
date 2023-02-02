import os


class Corpus:
    def __init__(self, dir_w_mails):
        self.dir_w_mails = dir_w_mails

    # Yield name and body of email
    def emails(self):
        for fname in os.listdir(self.dir_w_mails):
            if fname == '!truth.txt' or fname == '!prediction.txt':
                continue

            else:
                e = open(self.dir_w_mails + '/' + fname, 'r', encoding='UTF-8')
                body = e.read()
                e.close()
                yield fname, body


if __name__ == '__main__':
    folder = os.path.dirname(os.path.realpath(__file__)) + '/1'
    a = Corpus(folder)
    for fname, body in a.emails():
        print(fname, body, '\n*********************************\n')
