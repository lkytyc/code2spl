import numpy as np


class MetricsCalculator2:
    def __init__(self):
        pass

    def mrr(self, data):
        if type(data) != list and type(data) != tuple:
            raise Exception("The input type is invalid because it is not exactly a list or tuple.")

        if len(data) == 0:
            return 0.0, [0.0]

        if type(data) == tuple:
            sub_list, total_num = data
            sub_list = np.array(sub_list)

            if total_num == 0:
                return 0.0, [0.0]

            ranking_array = 1.0 / np.array(range(1, len(sub_list) + 1))
            mr_np = sub_list * ranking_array

            mr = 0.0
            for value in mr_np:
                if value > 0:
                    mr = value
                    break

            return mr, [mr]

        separate_result = []
        for sub_list, total_num in data:
            sub_list = np.array(sub_list)

            if total_num == 0:
                mr = 0.0
            else:
                ranking_array = 1.0 / np.array(range(1, len(sub_list) + 1))
                mr_np = sub_list * ranking_array
                mr = 0.0
                for value in mr_np:
                    if value > 0:
                        mr = value
                        break

            separate_result.append(mr)

        return np.mean(separate_result), separate_result

    def map(self, data):
        if type(data) != list and type(data) != tuple:
            raise Exception("Signals that the input type is invalid.")

        if len(data) == 0:
            return 0.0, [0.0]

        if type(data) == tuple:
            sub_list, total_num = data
            sub_list = np.array(sub_list)

            if total_num == 0:
                return 0.0, [0.0]

            ranking_array = 1.0 / np.array(range(1, len(sub_list) + 1))
            rank = 0
            rank_list = []
            for item in sub_list:
                if item != 0:
                    rank += 1
                    rank_list.append(rank)
                else:
                    rank_list.append(0)

            ap = float(np.sum(np.array(rank_list) * ranking_array * sub_list)) / total_num
            return ap, [ap]

        separate_result = []
        for sub_list, total_num in data:
            sub_list = np.array(sub_list)

            if total_num == 0:
                ap = 0.0
            else:
                ranking_array = 1.0 / np.array(range(1, len(sub_list) + 1))
                rank = 0
                rank_list = []
                for item in sub_list:
                    if item != 0:
                        rank += 1
                        rank_list.append(rank)
                    else:
                        rank_list.append(0)

                ap = float(np.sum(np.array(rank_list) * ranking_array * sub_list)) / total_num

            separate_result.append(ap)

        return np.mean(separate_result), separate_result

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
