import os
import utils
from confmat import BinaryConfusionMatrix as BCM


# Return quality of spam filter based on true and predicted dictionaries
def compute_quality_for_corpus(directory):
    # Create dict of true information about emails
    truth_dict = utils.read_classification_from_file(
        os.path.join(directory, "!truth.txt"))

    # Create dict of predicted information about emails
    pred_dict = utils.read_classification_from_file(
        os.path.join(directory, "!prediction.txt"))

    # Create BCM based on true and predicted dictionaries
    matrix = BCM(pos_tag="SPAM", neg_tag="OK")
    matrix.compute_from_dicts(truth_dict, pred_dict)
    return quality_score(matrix.as_dict()['tp'], matrix.as_dict()['tn'],
                         matrix.as_dict()['fp'], matrix.as_dict()['fn'])


# Return quality of spam filter based on binary classification
def quality_score(tp, tn, fp, fn):
    return (tp + tn) / (tp + tn + 10 * fp + fn)

