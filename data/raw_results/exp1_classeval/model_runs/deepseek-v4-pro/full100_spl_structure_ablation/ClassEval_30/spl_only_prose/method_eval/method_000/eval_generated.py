import numpy as np


class DataStatistics2:
    def __init__(self, data):
        self.data = np.array(data)

    def get_correlation(self):
        return np.corrcoef(self.data, rowvar=False)

    def get_max(self):
        return np.max(self.data)

    def get_min(self):
        return np.min(self.data)

    def get_std_deviation(self):
        std_deviation = np.std(self.data)
        rounded_std_deviation = round(std_deviation, 2)
        return rounded_std_deviation

    def get_sum(self):
        self_ref = self
        data_ref = self_ref.data
        sum_result = np.sum(data_ref)
        return sum_result

    def get_variance(self):
        rounded_variance = round(np.var(self.data), 2)
        return rounded_variance

import unittest

class DataStatistics2TestGetSum(unittest.TestCase):
    def test_get_sum_1(self):
        ds2 = DataStatistics2([1, 2, 3, 4])
        res = ds2.get_sum()
        self.assertEqual(res, 10)

    def test_get_sum_2(self):
        ds2 = DataStatistics2([1, 2, 203, 4])
        res = ds2.get_sum()
        self.assertEqual(res, 210)

    def test_get_sum_3(self):
        ds2 = DataStatistics2([1, 2, 33, 4])
        res = ds2.get_sum()
        self.assertEqual(res, 40)

    def test_get_sum_4(self):
        ds2 = DataStatistics2([1, 2, 333, 4])
        res = ds2.get_sum()
        self.assertEqual(res, 340)

    def test_get_sum_5(self):
        ds2 = DataStatistics2([1, 2, 6, 4])
        res = ds2.get_sum()
        self.assertEqual(res, 13)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
