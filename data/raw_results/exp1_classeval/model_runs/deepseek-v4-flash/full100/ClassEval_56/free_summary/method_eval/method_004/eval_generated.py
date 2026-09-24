class MetricsCalculator:
    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.fn = 0
        self.tn = 0

    def update(self, predicted_labels, true_labels):
        for p, t in zip(predicted_labels, true_labels):
            if p == 1 and t == 1:
                self.tp += 1
            elif p == 1 and t == 0:
                self.fp += 1
            elif p == 0 and t == 1:
                self.fn += 1
            else:
                self.tn += 1

    def precision(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        denominator = self.tp + self.fp
        return self.tp / denominator if denominator else 0.0

    def recall(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        denominator = self.tp + self.fn
        return self.tp / denominator if denominator else 0.0

    def accuracy(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        denominator = self.tp + self.fp + self.fn + self.tn
        return (self.tp + self.tn) / denominator if denominator else 0.0

    def f1_score(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        p = self.precision(predicted_labels, true_labels)
        r = self.recall(predicted_labels, true_labels)
        denominator = p + r
        return 2 * p * r / denominator if denominator else 0.0

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
