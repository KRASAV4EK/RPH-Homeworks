from random import randint
import basefilter
import quality


class NaiveFilter(basefilter.BaseFilter):
    """ For all emails filter set HAM """
    def create_dict(self):
        my_dict = {}
        for fname, body in self.corpus.emails():
            my_dict[fname] = "OK"
        return my_dict


class ParanoidFilter(basefilter.BaseFilter):
    """ For all emails filter set SPAM """
    def create_dict(self):
        my_dict = {}
        for fname, body in self.corpus.emails():
            my_dict[fname] = "SPAM"
        return my_dict


class RandomFilter(basefilter.BaseFilter):
    """ Filter randomly set for emails HAM or SPAM """
    def create_dict(self):
        my_dict = {}
        for fname, body in self.corpus.emails():
            if randint(0, 2):
                my_dict[fname] = "SPAM"
            else:
                my_dict[fname] = "OK"
        return my_dict


if __name__ == '__main__':
    import os
    folder = os.path.dirname(os.path.realpath(__file__)) + '/1'

    naive = NaiveFilter()
    naive.test(folder)
    print(quality.compute_quality_for_corpus(folder), '- Naive')

    paranoid = ParanoidFilter()
    paranoid.test(folder)
    print(quality.compute_quality_for_corpus(folder), '- Paranoid'  )

    rand = RandomFilter()
    rand.test(folder)
    print(quality.compute_quality_for_corpus(folder), '- Random')

    os.remove(folder + '/!prediction.txt')
