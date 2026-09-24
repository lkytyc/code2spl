class MetricsCalculator2:
    def __init__(self):
        pass

    def mrr(self, data):
        if not isinstance(data, (list, tuple)):
            raise Exception("Signals that the input type is invalid.")

        if len(data) == 0:
            return 0.0, [0.0]

        if isinstance(data, tuple):
            sub_list, total_num = data
            sub_list = __import__("numpy").array(sub_list)

            if total_num == 0:
                return 0.0, [0.0]

            mr_np = sub_list * (1.0 / __import__("numpy").arange(1, len(sub_list) + 1))
            mr = 0.0
            for value in mr_np:
                if value > 0:
                    mr = value
                    break
            return mr, [mr]

        separate_result = []
        for sub_list, total_num in data:
            sub_list = __import__("numpy").array(sub_list)

            if total_num == 0:
                mr = 0.0
            else:
                mr_np = sub_list * (1.0 / __import__("numpy").arange(1, len(sub_list) + 1))
                mr = 0.0
                for value in mr_np:
                    if value > 0:
                        mr = value
                        break
            separate_result.append(mr)

        return sum(separate_result) / len(separate_result), separate_result

    def map(self, data):
        if not isinstance(data, (list, tuple)):
            raise Exception("Indicates the input must be a tuple([0,...,1,...],int) or an iteration of list of tuple.")

        if len(data) == 0:
            return 0.0, [0.0]

        if isinstance(data, tuple):
            sub_list, total_num = data
            sub_list = __import__("numpy").array(sub_list)

            if total_num == 0:
                return 0.0, [0.0]

            ranking_array = 1.0 / __import__("numpy").arange(1, len(sub_list) + 1)
            ranks = []
            current_rank = 1
            for value in sub_list:
                if value != 0:
                    ranks.append(current_rank)
                    current_rank += 1
                else:
                    ranks.append(0)

            ap = sum(r * w for r, w in zip(ranks, ranking_array)) / total_num
            return ap, [ap]

        separate_result = []
        for sub_list, total_num in data:
            sub_list = __import__("numpy").array(sub_list)

            if total_num == 0:
                ap = 0.0
            else:
                ranking_array = 1.0 / __import__("numpy").arange(1, len(sub_list) + 1)
                ranks = []
                current_rank = 1
                for value in sub_list:
                    if value != 0:
                        ranks.append(current_rank)
                        current_rank += 1
                    else:
                        ranks.append(0)

                ap = sum(r * w for r, w in zip(ranks, ranking_array)) / total_num

            separate_result.append(ap)

        return sum(separate_result) / len(separate_result), separate_result

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
