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

    def precision(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        predicted_positives = self.true_positives + self.false_positives
        if predicted_positives == 0:
            return 0.0
        return self.true_positives / predicted_positives

    def recall(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        actual_positives = self.true_positives + self.false_negatives
        if actual_positives == 0:
            return 0.0
        return self.true_positives / actual_positives

    def f1_score(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        predicted_positives = self.true_positives + self.false_positives
        actual_positives = self.true_positives + self.false_negatives

        precision = 0.0 if predicted_positives == 0 else self.true_positives / predicted_positives
        recall = 0.0 if actual_positives == 0 else self.true_positives / actual_positives

        if precision == 0.0 and recall == 0.0:
            return 0.0
        return 2 * precision * recall / (precision + recall)

    def accuracy(self, predicted_labels, true_labels):
        self.update(predicted_labels, true_labels)
        total = (
            self.true_positives
            + self.false_positives
            + self.false_negatives
            + self.true_negatives
        )
        if total == 0:
            return 0.0
        return (self.true_positives + self.true_negatives) / total

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
