class MetricsCalculator2:
    @staticmethod
    def _as_queries(data):
        if isinstance(data, tuple):
            if len(data) == 0:
                return []
            return [data]
        if isinstance(data, list):
            return data
        raise TypeError("Input must be a tuple or a list of tuples")

    @staticmethod
    def MRR(data):
        queries = MetricsCalculator2._as_queries(data)
        if not queries:
            return 0.0, [0.0]

        scores = []
        for relevance_list, total_relevant in queries:
            if total_relevant == 0:
                scores.append(0.0)
                continue

            score = 0.0
            for i, rel in enumerate(relevance_list, start=1):
                if rel != 0:
                    score = 1.0 / i
                    break
            scores.append(score)

        return sum(scores) / len(scores), scores

    @staticmethod
    def MAP(data):
        queries = MetricsCalculator2._as_queries(data)
        if not queries:
            return 0.0, [0.0]

        scores = []
        for relevance_list, total_relevant in queries:
            if total_relevant == 0:
                scores.append(0.0)
                continue

            relevant_seen = 0
            precision_sum = 0.0
            for i, rel in enumerate(relevance_list, start=1):
                if rel != 0:
                    relevant_seen += 1
                    precision_sum += relevant_seen / i

            scores.append(precision_sum / total_relevant)

        return sum(scores) / len(scores), scores

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
