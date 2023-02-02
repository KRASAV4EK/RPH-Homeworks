import utils
from corpus import Corpus
from trainingcorpus import TrainingCorpus as TC
from collections import Counter


class MyFilter:
    """
    Spam filter depends on most used words from training folder and on
    'words.txt' file, which was made from test folders '1' and '2'.
    That file have most used words from spam and ham emails.
    """

    def __init__(self):
        self.words = []
        self.spam_array = []
        self.ham_array = []

    def train(self, train_corpus_dir):
        # Create a small array from words, which can be in spam and in ham
        words = os.path.dirname(os.path.realpath(__file__)) + "/words.txt"
        with open(words, 'r', encoding='UTF-8') as w:
            for word in w.read().split():
                self.words.append(word)

        # Some test output <3
        # print("Normal words! - ", self.words)

        spam_dictionary = {}
        # Go through all spam and add 'spam' words in spam_dictionary
        corpus = TC(train_corpus_dir)
        for fname, body in corpus.spams():
            # Go through all words in mail
            for word in body.split():
                # Delete some useless symbols and lower letters
                word = word.strip('\n').lower()
                for char in ".,!?:;'":
                    word = word.replace(char, "")

                # Add words to the spam dictionary
                if word.isalpha() and len(word) > 1 and word not in self.words:
                    if word in spam_dictionary:
                        spam_dictionary[word] += 1
                    else:
                        spam_dictionary[word] = 1

        ham_dictionary = {}
        # Go through all ham and add 'ham' words in ham_dictionary
        corpus = TC(train_corpus_dir)
        for fname, body in corpus.hams():
            # Go through all words in mail
            for word in body.split():
                # Delete some useless symbols and lower letters
                word = word.strip('\n').lower()
                for char in ".,!?:;'":
                    word = word.replace(char, "")

                # Add words to the ham dictionary
                if word.isalpha() and len(word) > 1 and word not in self.words:
                    if word in ham_dictionary:
                        ham_dictionary[word] += 1
                    else:
                        ham_dictionary[word] = 1

        # Some test output <3
        # print(spam_dictionary)
        # print(ham_dictionary)

        # Create counter from spam and ham dictionaries
        spam = Counter(spam_dictionary)
        ham = Counter(ham_dictionary)

        # Create arrays with most used 'spam' and 'ham' words
        for key in spam.most_common(200):
            self.spam_array.append(key[0])

        for key in ham.most_common(200):
            self.ham_array.append(key[0])

        # Some test output <3
        # print("Words from spam! - ", self.spam_array)
        # print("Words from ham! - ", self.ham_array)

    def test(self, test_corpus_dir):
        # Create corpus and directory for '!prediction.txt'
        corpus = Corpus(test_corpus_dir)
        prediction_directory = {}

        # Go through all emails from test directory
        for fname, body in corpus.emails():
            # Set counters for better decision between spam and ham
            spam = 0
            ham = 0
            for word in body.split():
                # Delete some useless symbols and lower letters
                word = word.strip('\n').lower()
                for char in ".,!?:;'":
                    word = word.replace(char, "")

                # Update counters, depending on training arrays
                if word.isalpha() and len(word) > 1:
                    if word in self.spam_array and word in self.ham_array:
                        continue
                    if word in self.spam_array:
                        spam += 17
                    elif word in self.ham_array or word in self.words:
                        ham += 1
                    else:
                        continue

            # Some test output <3
            # print("Spam - ", spam, "Ham - ", ham)

            # Deciding between 'spam' and 'ham',
            # depending on values in spam and ham
            if spam > ham + 35:
                prediction_directory[fname] = 'SPAM'
            else:
                prediction_directory[fname] = 'OK'

        # Create the '!prediction.txt' in test folder
        utils.write_classification_to_file(test_corpus_dir + '/!prediction.txt',
                                           prediction_directory)


if __name__ == '__main__':
    # Some test output <3
    import quality
    import confmat
    import time
    import os

    start_time = time.time()
    train_dir = os.path.dirname(os.path.realpath(__file__)) + '/1'
    test_dir = os.path.dirname(os.path.realpath(__file__)) + '/2'

    filter = MyFilter()
    filter.train(train_dir)
    filter.test(test_dir)
    print("Filter quality - \033[34m{}\033[0m".format(
          quality.compute_quality_for_corpus(test_dir)))

    matrix = confmat.BinaryConfusionMatrix('SPAM', 'OK')
    truth_dict = utils.read_classification_from_file(test_dir + '/!truth.txt')
    pred_dict = utils.read_classification_from_file(test_dir + '/!prediction.txt')
    matrix.compute_from_dicts(truth_dict, pred_dict)
    print("Filter matrix - ", matrix.as_dict())

    print("--- %s seconds ---" % (time.time() - start_time))

    # +++++++++++++++++++++++++++++++++++++++

    start_time = time.time()

    filter.train(test_dir)
    filter.test(train_dir)
    print("Filter quality - \033[34m{}\033[0m".format(
          quality.compute_quality_for_corpus(test_dir)))

    truth_dict = utils.read_classification_from_file(test_dir + '/!truth.txt')
    pred_dict = utils.read_classification_from_file(test_dir + '/!prediction.txt')
    matrix.compute_from_dicts(truth_dict, pred_dict)
    print("Filter matrix - ", matrix.as_dict())

    print("--- %s seconds ---" % (time.time() - start_time))
