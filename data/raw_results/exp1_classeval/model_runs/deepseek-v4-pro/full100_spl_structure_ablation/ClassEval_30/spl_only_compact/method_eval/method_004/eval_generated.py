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

class DataStatistics2TestGetStdDeviation(unittest.TestCase):
    def test_get_std_deviation_1(self):
        ds2 = DataStatistics2([1, 2, 3, 4])
        res = ds2.get_std_deviation()
        self.assertEqual(res, 1.12)

    def test_get_std_deviation_2(self):
        ds2 = DataStatistics2([1, 2, 203, 4])
        res = ds2.get_std_deviation()
        self.assertEqual(res, 86.9)

    def test_get_std_deviation_3(self):
        ds2 = DataStatistics2([1, 4, 3, 2])
        res = ds2.get_std_deviation()
        self.assertEqual(res, 1.12)

    def test_get_std_deviation_4(self):
        ds2 = DataStatistics2([11, 14, 13, 12])
        res = ds2.get_std_deviation()
        self.assertEqual(res, 1.12)

    def test_get_std_deviation_5(self):
        ds2 = DataStatistics2([111, 114, 113, 112])
        res = ds2.get_std_deviation()
        self.assertEqual(res, 1.12)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
