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
