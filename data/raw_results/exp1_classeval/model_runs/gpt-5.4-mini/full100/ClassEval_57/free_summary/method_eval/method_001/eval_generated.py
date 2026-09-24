class MetricsCalculator2:
    def __init__(self):
        pass

    @staticmethod
    def mrr(data):
        if not isinstance(data, (list, tuple)):
            raise Exception("Input must be a list or tuple")

        if len(data) == 0:
            return 0.0, [0.0]

        def _single_mrr(item):
            if not isinstance(item, tuple) or len(item) != 2:
                raise Exception("Each item must be a tuple of the form (sub_list, total_num)")
            sub_list, total_num = item
            if total_num == 0:
                return 0.0
            for idx, val in enumerate(sub_list, start=1):
                if val > 0:
                    return 1.0 / idx
            return 0.0

        if isinstance(data, tuple):
            value = _single_mrr(data)
            return value, [value]

        results = [_single_mrr(item) for item in data]
        mean_value = float(np.mean(results)) if len(results) > 0 else 0.0
        return mean_value, results

    @staticmethod
    def map(data):
        if not isinstance(data, (list, tuple)):
            raise Exception("Input must be a list or tuple")

        if len(data) == 0:
            return 0.0, [0.0]

        def _single_map(item):
            if not isinstance(item, tuple) or len(item) != 2:
                raise Exception("Each item must be a tuple of the form (sub_list, total_num)")
            sub_list, total_num = item
            if total_num == 0:
                return 0.0
            rank = 0
            total = 0.0
            for pos, val in enumerate(sub_list, start=1):
                if val != 0:
                    rank += 1
                    total += rank / pos
            return total / total_num

        if isinstance(data, tuple):
            value = _single_map(data)
            return value, [value]

        results = [_single_map(item) for item in data]
        mean_value = float(np.mean(results)) if len(results) > 0 else 0.0
        return mean_value, results

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
