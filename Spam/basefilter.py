import utils
import corpus


class BaseFilter:
    """ Basic spam filter """

    def __init__(self):
        pass

    def train(self, file):
        pass

    def test(self, test_dir):
        self.corpus = corpus.Corpus(test_dir)
        self.my_dict = self.create_dict()
        file = test_dir + '/!prediction.txt'
        utils.write_classification_to_file(file, self.my_dict)

    def create_dict(self):
        raise NotImplementedError
