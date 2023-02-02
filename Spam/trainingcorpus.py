from utils import read_classification_from_file
import os


# Some class for training spam filter
class TrainingCorpus:
    def __init__(self, folder):
        self.folder = folder

    # Return OK if is HAM, else SPAM
    def get_class(self, email):
        dict = read_classification_from_file(self.folder + '/!truth.txt')
        return dict[email]

    # Return True if HAM, else False
    def is_ham(self, email):
        if self.get_class(email) == 'OK':
            return True
        else:
            return False

    # Return True if SPAM, else False
    def is_spam(self, email):
        if self.get_class(email) == 'SPAM':
            return True
        else:
            return False

    # Yield name and body of SPAM
    def spams(self):
        array_w_spam = []
        for file in os.listdir(self.folder):
            if file == '!truth.txt' or file == '!prediction.txt':
                continue

            if self.is_spam(file):
                array_w_spam.append(file)

            else:
                continue

        for fname in array_w_spam:
            e = open(self.folder + '/' + fname, 'r', encoding='UTF-8')
            body = e.read()
            e.close()
            yield fname, body

    # Yield name and body of HAM
    def hams(self):
        array_w_ham = []
        for file in os.listdir(self.folder):
            if file == '!truth.txt' or file == '!prediction.txt':
                continue

            if self.is_ham(file):
                array_w_ham.append(file)
            else:
                continue

        for fname in array_w_ham:
            e = open(self.folder + '/' + fname, 'r', encoding='UTF-8')
            body = e.read()
            e.close()
            yield fname, body


if __name__ == '__main__':

    folder = os.path.dirname(os.path.realpath(__file__)) + '/1'
    spam = TrainingCorpus(folder)
    print("------------A column of spam!------------")
    for fname, body in spam.spams():
        print(fname)

    ham = TrainingCorpus(folder)
    print("------------A column of ham!------------")
    for fname, body in ham.hams():
        print(fname)
    print('*********************************')

    email = TrainingCorpus(folder)
    print(email.get_class('00271.85110ef4815c81ccea879857b0b062ed'))
    print(email.is_spam('00271.85110ef4815c81ccea879857b0b062ed'))
    print(email.is_ham('00271.85110ef4815c81ccea879857b0b062ed'))
