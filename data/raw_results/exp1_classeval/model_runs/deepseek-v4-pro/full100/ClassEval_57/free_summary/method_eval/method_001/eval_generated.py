class MetricsCalculator2:
    @staticmethod
    def mrr(data):
        if not isinstance(data, (list, tuple)):
            raise TypeError("Input must be a tuple or list of tuples")
        if isinstance(data, tuple):
            data = [data]
        if len(data) == 0:
            return 0.0, [0.0]
        reciprocal_ranks = []
        for sub_list, total_num in data:
            if total_num == 0:
                reciprocal_ranks.append(0.0)
                continue
            sub_list = list(sub_list)
            try:
                first_relevant = sub_list.index(1) + 1
                reciprocal_ranks.append(1.0 / first_relevant)
            except ValueError:
                reciprocal_ranks.append(0.0)
        mean_rr = float(np.mean(reciprocal_ranks)) if reciprocal_ranks else 0.0
        return mean_rr, reciprocal_ranks

    @staticmethod
    def map(data):
        if not isinstance(data, (list, tuple)):
            raise TypeError("Input must be a tuple or list of tuples")
        if isinstance(data, tuple):
            data = [data]
        if len(data) == 0:
            return 0.0, [0.0]
        average_precisions = []
        for sub_list, total_num in data:
            if total_num == 0:
                average_precisions.append(0.0)
                continue
            sub_list = np.array(sub_list)
            total_num = int(total_num)
            precisions = []
            relevant_count = 0
            for i, rel in enumerate(sub_list, start=1):
                if rel == 1:
                    relevant_count += 1
                    precisions.append(relevant_count / i)
            if precisions:
                avg_precision = np.mean(precisions)
            else:
                avg_precision = 0.0
            average_precisions.append(avg_precision)
        mean_ap = float(np.mean(average_precisions)) if average_precisions else 0.0
        return mean_ap, average_precisions

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
