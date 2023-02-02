class BinaryConfusionMatrix:
    """
    Build matrix based on Binary Classification
    """

    def __init__(self, pos_tag, neg_tag):
        self.pos_tag = pos_tag
        self.neg_tag = neg_tag
        self.matrix = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}

    # Return BCM
    def as_dict(self):
        return self.matrix

    # Update BCM based on truth and prediction
    def update(self, truth, prediction):
        # Update for positive tag
        if truth == self.pos_tag:
            if prediction == self.pos_tag:
                self.matrix['tp'] += 1
            elif prediction == self.neg_tag:
                self.matrix['fn'] += 1
            else:
                self.value_error(prediction)

        # Update for negative tag
        elif truth == self.neg_tag:
            if prediction == self.neg_tag:
                self.matrix['tn'] += 1
            elif prediction == self.pos_tag:
                self.matrix['fp'] += 1
            else:
                self.value_error(prediction)

        # Raise Error if nothing matched
        else:
            self.value_error(truth)

    # Update BCM based on true and predicted dictionaries
    def compute_from_dicts(self, truth_dict, pred_dict):
        for key in pred_dict:
            if key in truth_dict:
                self.update(truth_dict[key], pred_dict[key])

    # Raise the error if value isn't positive and negative tag
    def value_error(self, value):
        raise (ValueError("Error: bad parameter for update function: {}\n "
                          "Expected: {} or {}".format(value, self.pos_tag,
                                                      self.neg_tag)))


if __name__ == '__main__':
    cm1 = BinaryConfusionMatrix(pos_tag=True, neg_tag=False)
    print(cm1.as_dict())
    cm1.update(True, True)
    cm1.as_dict()
    truth_dict = {'em1': 'SPAM', 'em2': 'SPAM', 'em3': 'OK', 'em4': 'OK'}
    pred_dict = {'em1': 'SPAM', 'em2': 'OK', 'em3': 'OK', 'em4': 'SPAM'}
    cm2 = BinaryConfusionMatrix(pos_tag='SPAM', neg_tag='OK')
    cm2.compute_from_dicts(truth_dict, pred_dict)
    print(cm2.as_dict())

# tf-idf
