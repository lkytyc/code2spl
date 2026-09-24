class MetricsCalculator2:
    def __init__(self):
        pass

    @staticmethod
    def mrr(data):
        import numpy as np

        if not isinstance(data, (list, tuple)):
            raise Exception("Input must be a list or tuple.")

        if len(data) == 0:
            return 0.0, [0.0]

        def _calc_one(item):
            sub_list, total_num = item
            if total_num == 0:
                return 0.0
            rel = np.array(sub_list)
            weights = 1.0 / np.arange(1, len(rel) + 1)
            scores = rel * weights
            positives = np.where(scores > 0)[0]
            return float(scores[positives[0]]) if len(positives) > 0 else 0.0

        if isinstance(data, tuple):
            value = _calc_one(data)
            return value, [value]

        values = [_calc_one(item) for item in data]
        return float(np.mean(values)) if len(values) > 0 else 0.0, values

    @staticmethod
    def map(data):
        import numpy as np

        if not isinstance(data, (list, tuple)):
            raise Exception("Input must be a list or tuple.")

        if len(data) == 0:
            return 0.0, [0.0]

        def _calc_one(item):
            sub_list, total_num = item
            if total_num == 0:
                return 0.0
            rel = np.array(sub_list)
            running = 0
            rel_counts = []
            for x in rel:
                if x != 0:
                    running += 1
                    rel_counts.append(running)
                else:
                    rel_counts.append(0)
            rel_counts = np.array(rel_counts)
            weights = 1.0 / np.arange(1, len(rel_counts) + 1)
            ap = np.sum(rel_counts * weights) / total_num
            return float(ap)

        if isinstance(data, tuple):
            value = _calc_one(data)
            return value, [value]

        values = [_calc_one(item) for item in data]
        return float(np.mean(values)) if len(values) > 0 else 0.0, values

import unittest

class MetricsCalculator2TestMrr(unittest.TestCase):
    def test_mrr_1(self):
        mc2 = MetricsCalculator2()
        res1, res2 = MetricsCalculator2.mrr(([1, 0, 1, 0], 4))
        self.assertEqual(res1, 1.0)
        self.assertEqual(res2, [1.0])

    def test_mrr_2(self):
        res1, res2 = MetricsCalculator2.mrr(([0, 0, 0, 1], 4))
        self.assertEqual(res1, 0.25)
        self.assertEqual(res2, [0.25])

    def test_mrr_3(self):
        res1, res2 = MetricsCalculator2.mrr([([1, 0, 1, 0], 4), ([0, 1, 0, 1], 4)])
        self.assertEqual(res1, 0.75)
        self.assertEqual(res2, [1.0, 0.5])

    def test_mrr_4(self):
        res1, res2 = MetricsCalculator2.mrr([([1, 1, 1, 0], 4), ([0, 0, 0, 1], 4)])
        self.assertEqual(res1, 0.625)
        self.assertEqual(res2, [1.0, 0.25])

    def test_mrr_5(self):
        res1, res2 = MetricsCalculator2.mrr([([1, 0, 1, 1], 4), ([0, 1, 0, 0], 4)])
        self.assertEqual(res1, 0.75)
        self.assertEqual(res2, [1.0, 0.5])

    def test_mrr_6(self):
        try:
            MetricsCalculator2.mrr(1)
        except:
            pass

    def test_mrr_7(self):
        res1, res2 = MetricsCalculator2.mrr([])
        self.assertEqual(res1, 0.0)
        self.assertEqual(res2, [0.0])

    def test_mrr_8(self):
        res1, res2 = MetricsCalculator2.mrr([([1, 0, 1, 1], 0), ([0, 1, 0, 0], 0)])
        self.assertEqual(res1, 0.0)
        self.assertEqual(res2, [0.0, 0.0])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
