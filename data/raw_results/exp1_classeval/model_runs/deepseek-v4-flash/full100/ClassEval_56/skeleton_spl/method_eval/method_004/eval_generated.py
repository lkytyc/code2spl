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
        """
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
        """
        self.update(predicted_labels, true_labels)
        if self.true_positives + self.false_positives == 0:
            return 0.0
        return self.true_positives / (self.true_positives + self.false_positives)

    def recall(self, predicted_labels, true_labels):
        """
        Calculate recall
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        """
        self.update(predicted_labels, true_labels)
        if self.true_positives + self.false_negatives == 0:
            return 0.0
        return self.true_positives / (self.true_positives + self.false_negatives)

    def f1_score(self, predicted_labels, true_labels):
        """
        Calculate f1 score, which is the harmonic mean of precision and recall
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        """
        self.update(predicted_labels, true_labels)
        precision_value = self.precision(predicted_labels, true_labels)
        recall_value = self.recall(predicted_labels, true_labels)
        if precision_value + recall_value == 0.0:
            return 0.0
        return (2 * precision_value * recall_value) / (precision_value + recall_value)

    def accuracy(self, predicted_labels, true_labels):
        """
        Calculate accuracy
        :param predicted_labels: list, predicted results
        :param true_labels: list, true labels
        :return: float
        """
        self.update(predicted_labels, true_labels)
        total = self.true_positives + self.true_negatives + self.false_positives + self.false_negatives
        if total == 0:
            return 0.0
        return (self.true_positives + self.true_negatives) / total

import unittest

class MetricsCalculatorTestAccuracy(unittest.TestCase):
    def test_accuracy_1(self):
        mc = MetricsCalculator()
        temp = mc.accuracy([1, 1, 0, 0], [1, 0, 0, 1])
        self.assertEqual(temp, 0.5)

    def test_accuracy_2(self):
        mc = MetricsCalculator()
        temp = mc.accuracy([1, 1, 2, 0], [1, 0, 0, 1])
        self.assertAlmostEqual(temp, 0.3333333333333333)

    def test_accuracy_3(self):
        mc = MetricsCalculator()
        temp = mc.accuracy([1, 1, 0, 1], [1, 0, 0, 1])
        self.assertEqual(temp, 0.75)

    def test_accuracy_4(self):
        mc = MetricsCalculator()
        temp = mc.accuracy([1, 1, 0, 0], [1, 1, 0, 1])
        self.assertEqual(temp, 0.75)

    def test_accuracy_5(self):
        mc = MetricsCalculator()
        temp = mc.accuracy([1, 1, 0, 0], [1, 0, 1, 1])
        self.assertEqual(temp, 0.25)

    def test_accuracy_6(self):
        mc = MetricsCalculator()
        temp = mc.accuracy([], [])
        self.assertEqual(temp, 0.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
