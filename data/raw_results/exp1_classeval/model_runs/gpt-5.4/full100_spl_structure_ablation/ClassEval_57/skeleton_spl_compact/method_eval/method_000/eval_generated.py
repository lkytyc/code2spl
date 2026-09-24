class MetricsCalculator2:
    """
    The class provides to calculate Mean Reciprocal Rank (MRR) and Mean Average Precision (MAP) based on input data, where MRR measures the ranking quality and MAP measures the average precision.
    """

    def __init__(self):
        pass

    @staticmethod
    def mrr(data):
        """
        compute the MRR of the input data. MRR is a widely used evaluation index. It is the mean of reciprocal rank.
        """
        if type(data) not in (list, tuple):
            raise Exception(
                "The input type is invalid because it is not exactly a list or tuple."
            )

        if len(data) == 0:
            return 0.0, [0.0]

        if type(data) is tuple:
            sub_list, total_num = data
            sub_list = np.asarray(sub_list)

            if total_num == 0:
                return 0.0, [0.0]

            ranking_array = 1.0 / np.arange(1, len(sub_list) + 1)
            mr_np = sub_list * ranking_array
            mr = 0.0

            for value in mr_np:
                if value > 0:
                    mr = value
                    break

            return mr, [mr]

        separate_result = []

        for sub_list, total_num in data:
            sub_list = np.asarray(sub_list)

            if total_num == 0:
                mr = 0.0
            else:
                ranking_array = 1.0 / np.arange(1, len(sub_list) + 1)
                mr_np = sub_list * ranking_array
                mr = 0.0

                for value in mr_np:
                    if value > 0:
                        mr = value
                        break

            separate_result.append(mr)

        return np.mean(separate_result), separate_result

    @staticmethod
    def map(data):
        """
        compute the MAP of the input data. MAP is a widely used evaluation index. MAP is the mean of AP.
        """
        if type(data) not in (list, tuple):
            raise Exception("Signals that the input type is invalid.")

        if len(data) == 0:
            return 0.0, [0.0]

        if type(data) is tuple:
            sub_list, total_num = data
            sub_list = np.asarray(sub_list)

            if total_num == 0:
                return 0.0, [0.0]

            ranking_array = 1.0 / np.arange(1, len(sub_list) + 1)
            ranks = np.cumsum(sub_list != 0) * (sub_list != 0)
            ap = np.sum(ranking_array * ranks) / total_num

            return ap, [ap]

        separate_result = []

        for sub_list, total_num in data:
            sub_list = np.asarray(sub_list)

            if total_num == 0:
                ap = 0.0
            else:
                ranking_array = 1.0 / np.arange(1, len(sub_list) + 1)
                ranks = np.cumsum(sub_list != 0) * (sub_list != 0)
                ap = np.sum(ranking_array * ranks) / total_num

            separate_result.append(ap)

        return np.mean(separate_result), separate_result

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
