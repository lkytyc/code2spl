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
