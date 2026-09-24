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

class MetricsCalculator2TestMap(unittest.TestCase):
    def test_map_1(self):
        res1, res2 = MetricsCalculator2.map(([1, 0, 1, 0], 4))
        self.assertEqual(res1, 0.41666666666666663)
        self.assertEqual(res2, [0.41666666666666663])

    def test_map_2(self):
        res1, res2 = MetricsCalculator2.map(([0, 0, 0, 1], 4))
        self.assertEqual(res1, 0.0625)
        self.assertEqual(res2, [0.0625])

    def test_map_3(self):
        res1, res2 = MetricsCalculator2.map([([1, 0, 1, 0], 4), ([0, 1, 0, 1], 4)])
        self.assertEqual(res1, 0.3333333333333333)
        self.assertEqual(res2, [0.41666666666666663, 0.25])

    def test_map_4(self):
        res1, res2 = MetricsCalculator2.map([([1, 1, 1, 0], 4), ([0, 0, 0, 1], 4)])
        self.assertEqual(res1, 0.40625)
        self.assertEqual(res2, [0.75, 0.0625])

    def test_map_5(self):
        res1, res2 = MetricsCalculator2.map([([1, 0, 1, 1], 4), ([0, 1, 0, 0], 4)])
        self.assertEqual(res1, 0.3645833333333333)
        self.assertEqual(res2, [0.6041666666666666, 0.125])

    def test_map_6(self):
        try:
            MetricsCalculator2.map(1)
        except:
            pass

    def test_map_7(self):
        res1, res2 = MetricsCalculator2.map([])
        self.assertEqual(res1, 0.0)
        self.assertEqual(res2, [0.0])

    def test_map_8(self):
        res1, res2 = MetricsCalculator2.map([([1, 0, 1, 1], 0), ([0, 1, 0, 0], 0)])
        self.assertEqual(res1, 0.0)
        self.assertEqual(res2, [0.0, 0.0])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
