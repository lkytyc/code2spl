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
