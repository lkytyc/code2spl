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
