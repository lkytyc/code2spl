class MetricsCalculator:
    def __init__(self):
        self.true_positives = 0
        self.false_positives = 0
        self.false_negatives = 0
        self.true_negatives = 0

    def update(self, predictions, labels):
        for pred, true in zip(predictions, labels):
            if pred == 1 and true == 1:
                self.true_positives += 1
            elif pred == 1 and true == 0:
                self.false_positives += 1
            elif pred == 0 and true == 1:
                self.false_negatives += 1
            elif pred == 0 and true == 0:
                self.true_negatives += 1

    def precision(self, predictions, labels):
        self.update(predictions, labels)
        denominator = self.true_positives + self.false_positives
        if denominator == 0:
            return 0.0
        return self.true_positives / denominator

    def recall(self, predictions, labels):
        self.update(predictions, labels)
        denominator = self.true_positives + self.false_negatives
        if denominator == 0:
            return 0.0
        return self.true_positives / denominator

    def f1_score(self, predictions, labels):
        self.update(predictions, labels)
        p = self.precision([], [])
        r = self.recall([], [])
        if p + r == 0:
            return 0.0
        return 2 * (p * r) / (p + r)

    def accuracy(self, predictions, labels):
        self.update(predictions, labels)
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
