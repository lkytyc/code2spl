class MetricsCalculator:
    def __init__(self):
        self.true_positives = 0
        self.false_positives = 0
        self.false_negatives = 0
        self.true_negatives = 0

    def update(self, predicted_labels, true_labels):
        for predicted, true in zip(predicted_labels, true_labels):
            if predicted == 1 and true == 1:
                self.true_positives += 1
            elif predicted == 1 and true == 0:
                self.false_positives += 1
            elif predicted == 0 and true == 1:
                self.false_negatives += 1
            elif predicted == 0 and true == 0:
                self.true_negatives += 1

    def accuracy(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        total = self.true_positives + self.true_negatives + self.false_positives + self.false_negatives
        if total == 0:
            return 0.0
        return (self.true_positives + self.true_negatives) / total

    def precision(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        if self.true_positives + self.false_positives == 0:
            return 0.0
        return self.true_positives / (self.true_positives + self.false_positives)

    def recall(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        if self.true_positives + self.false_negatives == 0:
            return 0.0
        return self.true_positives / (self.true_positives + self.false_negatives)

    def f1_score(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        precision = self.precision(predicted_labels, true_labels)
        recall = self.recall(predicted_labels, true_labels)
        if precision + recall == 0.0:
            return 0.0
        return (2 * precision * recall) / (precision + recall)

import unittest

class MetricsCalculatorTestRecall(unittest.TestCase):
    def test_recall_1(self):
        mc = MetricsCalculator()
        temp = mc.recall([1, 1, 0, 0], [1, 0, 0, 1])
        self.assertEqual(temp, 0.5)

    def test_recall_2(self):
        mc = MetricsCalculator()
        temp = mc.recall([1, 1, 1, 0], [1, 0, 0, 1])
        self.assertEqual(temp, 0.5)

    def test_recall_3(self):
        mc = MetricsCalculator()
        temp = mc.recall([1, 1, 0, 1], [1, 0, 0, 1])
        self.assertEqual(temp, 1.0)

    def test_recall_4(self):
        mc = MetricsCalculator()
        temp = mc.recall([1, 1, 0, 0], [1, 1, 0, 1])
        self.assertAlmostEqual(temp, 0.6666666666666666)

    def test_recall_5(self):
        mc = MetricsCalculator()
        temp = mc.recall([1, 1, 0, 0], [1, 0, 1, 1])
        self.assertAlmostEqual(temp, 0.3333333333333333)

    def test_recall_6(self):
        mc = MetricsCalculator()
        temp = mc.recall([1, 1, 0, 0], [0, 0, 0, 0])
        self.assertEqual(temp, 0.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
