class MetricsCalculator:
    """
    The class calculates precision, recall, F1 score, and accuracy based on predicted and true labels.
    """

    def __init__(self):
        """
        Initialize the number of all four samples to 0
        """
        self.true_positives = 0
        self.false_positives = 0
        self.false_negatives = 0
        self.true_negatives = 0

    def update(self, predicted_labels, true_labels):
        """
        Update the number of all four samples(true_positives, false_positives, false_negatives, true_negatives)
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: None, change the number of corresponding samples
        >>> mc = MetricsCalculator()
        >>> mc.update([1, 1, 0, 0], [1, 0, 0, 1])
        (self.true_positives, self.false_positives, self.false_negatives, self.true_negatives) = (1, 1, 1, 1)
        """
        for p, t in zip(predicted_labels, true_labels):
            if p == 1:
                if t == 1:
                    self.true_positives += 1
                else:
                    self.false_positives += 1
            else:
                if t == 1:
                    self.false_negatives += 1
                else:
                    self.true_negatives += 1

    def precision(self, predicted_labels, true_labels):
        """
        Calculate precision
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        >>> mc = MetricsCalculator()
        >>> mc.precision([1, 1, 0, 0], [1, 0, 0, 1])
        0.5
        """
        tp = 0
        fp = 0
        for p, t in zip(predicted_labels, true_labels):
            if p == 1 and t == 1:
                tp += 1
            elif p == 1 and t == 0:
                fp += 1
        if tp + fp == 0:
            return 0.0
        return tp / (tp + fp)

    def recall(self, predicted_labels, true_labels):
        """
        Calculate recall
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        >>> mc = MetricsCalculator()
        >>> mc.recall([1, 1, 0, 0], [1, 0, 0, 1])
        0.5
        """
        tp = 0
        fn = 0
        for p, t in zip(predicted_labels, true_labels):
            if p == 1 and t == 1:
                tp += 1
            elif p == 0 and t == 1:
                fn += 1
        if tp + fn == 0:
            return 0.0
        return tp / (tp + fn)

    def f1_score(self, predicted_labels, true_labels):
        """
        Calculate f1 score, which is the harmonic mean of precision and recall
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        >>> mc = MetricsCalculator()
        >>> mc.f1_score([1, 1, 0, 0], [1, 0, 0, 1])
        0.5
        """
        precision = self.precision(predicted_labels, true_labels)
        recall = self.recall(predicted_labels, true_labels)
        if precision + recall == 0:
            return 0.0
        return 2 * precision * recall / (precision + recall)

    def accuracy(self, predicted_labels, true_labels):
        """
        Calculate accuracy
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        >>> mc = MetricsCalculator()
        >>>mc.accuracy([1, 1, 0, 0], [1, 0, 0, 1])
        0.5
        """
        correct = 0
        total = 0
        for p, t in zip(predicted_labels, true_labels):
            total += 1
            if p == t:
                correct += 1
        if total == 0:
            return 0.0
        return correct / total

import unittest

class MetricsCalculatorTestF1Score(unittest.TestCase):
    def test_f1_score_1(self):
        mc = MetricsCalculator()
        temp = mc.f1_score([1, 1, 0, 0], [1, 0, 0, 1])
        self.assertEqual(temp, 0.5)

    def test_f1_score_2(self):
        mc = MetricsCalculator()
        temp = mc.f1_score([1, 1, 1, 0], [1, 0, 0, 1])
        self.assertEqual(temp, 0.4)

    def test_f1_score_3(self):
        mc = MetricsCalculator()
        temp = mc.f1_score([1, 1, 0, 1], [1, 0, 0, 1])
        self.assertEqual(temp, 0.8)

    def test_f1_score_4(self):
        mc = MetricsCalculator()
        temp = mc.f1_score([1, 1, 0, 0], [1, 1, 0, 1])
        self.assertEqual(temp, 0.8)

    def test_f1_score_5(self):
        mc = MetricsCalculator()
        temp = mc.f1_score([1, 1, 0, 0], [1, 0, 1, 1])
        self.assertEqual(temp, 0.4)

    def test_f1_score_6(self):
        mc = MetricsCalculator()
        temp = mc.f1_score([0, 0, 0, 0], [0, 0, 0, 0])
        self.assertEqual(temp, 0.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
