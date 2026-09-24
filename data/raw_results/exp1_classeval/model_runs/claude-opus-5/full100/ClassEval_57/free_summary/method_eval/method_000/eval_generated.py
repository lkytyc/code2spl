class MetricsCalculator2:

    @staticmethod
    def mrr(rs):
        if not rs:
            return 0.0, []

        # Normalize single tuple to list
        if isinstance(rs, tuple):
            rs = [rs]

        scores = []
        for sub_list, total_num in rs:
            if total_num == 0 or not sub_list:
                scores.append(0.0)
                continue

            rr_array = [1.0 / (i + 1) for i in range(len(sub_list))]
            products = [rr * rel for rr, rel in zip(rr_array, sub_list)]

            score = 0.0
            for p in products:
                if p != 0.0:
                    score = p
                    break

            scores.append(score)

        if not scores:
            return 0.0, []

        return sum(scores) / len(scores), scores

    @staticmethod
    def map(rs):
        if not rs:
            return 0.0, []

        # Normalize single tuple to list
        if isinstance(rs, tuple):
            rs = [rs]

        scores = []
        for sub_list, total_num in rs:
            if total_num == 0 or not sub_list:
                scores.append(0.0)
                continue

            rr_array = [1.0 / (i + 1) for i in range(len(sub_list))]

            right_ranking_list = []
            count = 0
            for rel in sub_list:
                if rel != 0:
                    count += 1
                    right_ranking_list.append(count)
                else:
                    right_ranking_list.append(0)

            ap = sum(r * rr for r, rr in zip(right_ranking_list, rr_array)) / total_num
            scores.append(ap)

        if not scores:
            return 0.0, []

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
