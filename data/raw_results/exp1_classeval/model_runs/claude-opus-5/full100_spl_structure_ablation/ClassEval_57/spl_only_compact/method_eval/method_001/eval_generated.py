import numpy as np


class MetricsCalculator2:

    def __init__(self):
        pass

    def map(self, data):
        # Step 1: type guard
        if not isinstance(data, (list, tuple)):
            raise Exception('the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple')

        # Step 2: empty guard
        if len(data) == 0:
            return 0.0, [0.0]

        # Step 3: tuple branch (strict type check)
        if type(data) == tuple:
            sub_list, total_num = data
            sub_list = np.array(sub_list)

            # Step 4: zero guard
            if total_num == 0:
                return 0.0, [0.0]

            # Step 5: ranking array
            ranking_array = 1.0 / (np.array(range(len(sub_list))) + 1)

            # Step 6: right ranking list
            right_ranking_list = []
            count = 1
            for t in sub_list:
                if t == 0:
                    right_ranking_list.append(0)
                else:
                    right_ranking_list.append(count)
                    count += 1

            # Step 7: compute ap and return
            ap = np.dot(right_ranking_list, ranking_array) / total_num
            return ap, [ap]

        # Step 8: list branch (strict type check)
        if type(data) == list:
            separate_result = []

            # Step 9: iterate over pairs
            for sub_list, total_num in data:
                sub_list = np.array(sub_list)

                # Step 10: zero guard
                if total_num == 0:
                    ap = 0.0
                else:
                    # Step 11: ranking array
                    ranking_array = 1.0 / (np.array(range(len(sub_list))) + 1)

                    # Step 12: right ranking list
                    right_ranking_list = []
                    count = 1
                    for t in sub_list:
                        if t == 0:
                            right_ranking_list.append(0)
                        else:
                            right_ranking_list.append(count)
                            count += 1

                    # Step 13: compute ap
                    ap = np.dot(right_ranking_list, ranking_array) / total_num

                # Step 14: accumulate
                separate_result.append(ap)

            # Step 15: return mean and breakdown
            return np.mean(separate_result), separate_result

    def mrr(self, data):
        # Step 1: type guard
        if not isinstance(data, (list, tuple)):
            raise Exception('the input must be a tuple([0,...,1,...],int) or a iteration of list of tuple')

        # Step 2: empty guard
        if len(data) == 0:
            return 0.0, [0.0]

        # Step 3: tuple branch (strict type check)
        if type(data) == tuple:
            # Step 4: unpack
            sub_list, total_num = data
            sub_list = np.array(sub_list)

            # Step 5: zero guard
            if total_num == 0:
                return 0.0, [0.0]
            else:
                # Step 6: ranking array
                ranking_array = 1.0 / (np.array(range(len(sub_list))) + 1)

                # Step 7: element-wise product
                mr_np = sub_list * ranking_array

                # Step 8: first-hit scan
                mr = 0.0
                for team in mr_np:
                    if team > 0:
                        mr = team
                        break

                # Step 9: return
                return mr, [mr]

        # Step 10: list branch (strict type check)
        if type(data) == list:
            # Step 11: init
            separate_result = []

            # Step 12: iterate
            for sub_list, total_num in data:
                sub_list = np.array(sub_list)

                # Step 13: zero guard
                if total_num == 0:
                    mr = 0.0
                else:
                    # Step 14: ranking array
                    ranking_array = 1.0 / (np.array(range(len(sub_list))) + 1)

                    # Step 15: element-wise product
                    mr_np = sub_list * ranking_array

                    # Step 16: first-hit scan
                    mr = 0.0
                    for team in mr_np:
                        if team > 0:
                            mr = team
                            break

                # Step 17: append
                separate_result.append(mr)

            # Step 18: return
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
