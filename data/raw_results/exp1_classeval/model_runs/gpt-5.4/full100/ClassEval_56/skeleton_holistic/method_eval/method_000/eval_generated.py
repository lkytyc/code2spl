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
        if len(predicted_labels) != len(true_labels):
            raise ValueError("predicted_labels and true_labels must have the same length")

        self.true_positives = 0
        self.false_positives = 0
        self.false_negatives = 0
        self.true_negatives = 0

        for predicted, true in zip(predicted_labels, true_labels):
            if predicted == 1 and true == 1:
                self.true_positives += 1
            elif predicted == 1 and true == 0:
                self.false_positives += 1
            elif predicted == 0 and true == 1:
                self.false_negatives += 1
            elif predicted == 0 and true == 0:
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
        self.update(predicted_labels, true_labels)
        denominator = self.true_positives + self.false_positives
        if denominator == 0:
            return 0.0
        return self.true_positives / denominator

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
        self.update(predicted_labels, true_labels)
        denominator = self.true_positives + self.false_negatives
        if denominator == 0:
            return 0.0
        return self.true_positives / denominator

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
        denominator = precision + recall
        if denominator == 0:
            return 0.0
        return 2 * precision * recall / denominator

    def accuracy(self, predicted_labels, true_labels):
        """
        Calculate accuracy
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        >>>mc.accuracy([1, 1, 0, 0], [1, 0, 0, 1])
        0.5
        """
        self.update(predicted_labels, true_labels)
        total = self.true_positives + self.false_positives + self.false_negatives + self.true_negatives
        if total == 0:
            return 0.0
        return (self.true_positives + self.true_negatives) / total

import unittest

class MetricsCalculatorTestUpdate(unittest.TestCase):
    def test_update_1(self):
        mc = MetricsCalculator()
        self.assertEqual((mc.true_positives, mc.false_positives, mc.false_negatives, mc.true_negatives), (0, 0, 0, 0))
        mc.update([1, 1, 0, 0], [1, 0, 0, 1])
        self.assertEqual((mc.true_positives, mc.false_positives, mc.false_negatives, mc.true_negatives), (1, 1, 1, 1))

    def test_update_2(self):
        mc = MetricsCalculator()
        self.assertEqual((mc.true_positives, mc.false_positives, mc.false_negatives, mc.true_negatives), (0, 0, 0, 0))
        mc.update([1, 1, 1, 0], [1, 0, 0, 1])
        self.assertEqual((mc.true_positives, mc.false_positives, mc.false_negatives, mc.true_negatives), (1, 2, 1, 0))

    def test_update_3(self):
        mc = MetricsCalculator()
        self.assertEqual((mc.true_positives, mc.false_positives, mc.false_negatives, mc.true_negatives), (0, 0, 0, 0))
        mc.update([1, 1, 0, 1], [1, 0, 0, 1])
        self.assertEqual((mc.true_positives, mc.false_positives, mc.false_negatives, mc.true_negatives), (2, 1, 0, 1))

    def test_update_4(self):
        mc = MetricsCalculator()
        self.assertEqual((mc.true_positives, mc.false_positives, mc.false_negatives, mc.true_negatives), (0, 0, 0, 0))
        mc.update([1, 1, 0, 0], [1, 1, 0, 1])
        self.assertEqual((mc.true_positives, mc.false_positives, mc.false_negatives, mc.true_negatives), (2, 0, 1, 1))

    def test_update_5(self):
        mc = MetricsCalculator()
        self.assertEqual((mc.true_positives, mc.false_positives, mc.false_negatives, mc.true_negatives), (0, 0, 0, 0))
        mc.update([1, 1, 0, 0], [1, 0, 1, 1])
        self.assertEqual((mc.true_positives, mc.false_positives, mc.false_negatives, mc.true_negatives), (1, 1, 2, 0))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
