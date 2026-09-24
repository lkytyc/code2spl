class MetricsCalculator2:
    def __init__(self):
        return

    def map(self, data):
        import numpy as np

        if not isinstance(data, (list, tuple)):
            raise Exception("Indicates the input must be a tuple([0,...,1,...],int) or an iteration of list of tuple.")

        if len(data) == 0:
            return 0.0, [0.0]

        if isinstance(data, tuple):
            sub_list, total_num = data
            sub_list = np.array(sub_list)

            if total_num == 0:
                return 0.0, [0.0]

            ranking_array = 1.0 / np.arange(1, len(sub_list) + 1)
            ranks = np.array([i + 1 if v != 0 else 0 for i, v in enumerate(sub_list)])
            ap = float(np.sum(ranks * ranking_array) / total_num)
            return ap, [ap]

        if isinstance(data, list):
            separate_result = []
            for sub_list, total_num in data:
                sub_list = np.array(sub_list)

                if total_num == 0:
                    ap = 0.0
                else:
                    ranking_array = 1.0 / np.arange(1, len(sub_list) + 1)
                    ranks = np.array([i + 1 if v != 0 else 0 for i, v in enumerate(sub_list)])
                    ap = float(np.sum(ranks * ranking_array) / total_num)
                separate_result.append(ap)

            return float(np.mean(separate_result)), separate_result

        raise Exception("Indicates the input must be a tuple([0,...,1,...],int) or an iteration of list of tuple.")

    def mrr(self, data):
        import numpy as np

        if not isinstance(data, (list, tuple)):
            raise Exception("Signals that the input type is invalid.")

        if len(data) == 0:
            return 0.0, [0.0]

        if isinstance(data, tuple):
            sub_list, total_num = data
            sub_list = np.array(sub_list)

            if total_num == 0:
                return 0.0, [0.0]

            reciprocal_weights = 1.0 / np.arange(1, len(sub_list) + 1)
            mr_np = sub_list * reciprocal_weights

            mr = 0.0
            for value in mr_np:
                if value > 0:
                    mr = float(value)
                    break

            return mr, [mr]

        if isinstance(data, list):
            separate_result = []
            for sub_list, total_num in data:
                sub_list = np.array(sub_list)

                if total_num == 0:
                    mr = 0.0
                else:
                    reciprocal_weights = 1.0 / np.arange(1, len(sub_list) + 1)
                    mr_np = sub_list * reciprocal_weights

                    mr = 0.0
                    for value in mr_np:
                        if value > 0:
                            mr = float(value)
                            break

                separate_result.append(mr)

            return float(np.mean(separate_result)), separate_result

        raise Exception("Signals that the input type is invalid.")

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


class MetricsCalculator2Test(unittest.TestCase):
    def test_metricscalculator2_1(self):
        res1, res2 = MetricsCalculator2.mrr(([1, 0, 1, 0], 4))
        self.assertEqual(res1, 1.0)
        self.assertEqual(res2, [1.0])

    def test_metricscalculator2_2(self):
        res1, res2 = MetricsCalculator2.mrr([([1, 0, 1, 0], 4), ([0, 1, 0, 1], 4)])
        self.assertEqual(res1, 0.75)
        self.assertEqual(res2, [1.0, 0.5])

    def test_metricscalculator2_3(self):
        res1, res2 = MetricsCalculator2.map(([1, 0, 1, 0], 4))
        self.assertEqual(res1, 0.41666666666666663)
        self.assertEqual(res2, [0.41666666666666663])

    def test_metricscalculator2_4(self):
        res1, res2 = MetricsCalculator2.map([([1, 0, 1, 0], 4), ([0, 1, 0, 1], 4)])
        self.assertEqual(res1, 0.3333333333333333)
        self.assertEqual(res2, [0.41666666666666663, 0.25])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
