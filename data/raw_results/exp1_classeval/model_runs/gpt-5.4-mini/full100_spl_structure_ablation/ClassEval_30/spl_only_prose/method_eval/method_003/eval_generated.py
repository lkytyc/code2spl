import numpy as np


class DataStatistics2:
    def __init__(self, data) -> None:
        array_data = np.array(data)
        self.data = array_data

    def get_correlation(self):
        correlation_matrix = np.corrcoef(self.data, rowvar=False)
        return correlation_matrix

    def get_max(self: object):
        data = self.data
        max_value = np.max(data)
        return max_value

    def get_min(self):
        data = self.data
        min_value = np.min(data)
        return min_value

    def get_std_deviation(self) -> float:
        data = self.data
        std_value = np.std(data)
        rounded_std = round(std_value, 2)
        return rounded_std

    def get_sum(self: object):
        data = self.data
        sum_value = np.sum(data)
        return sum_value

    def get_variance(self: object):
        data = self.data
        variance = np.var(data)
        rounded_variance = round(variance, 2)
        return rounded_variance

import unittest

class DataStatistics2TestGetVariance(unittest.TestCase):
    def test_get_variance_1(self):
        ds2 = DataStatistics2([1, 2, 3, 4])
        res = ds2.get_variance()
        self.assertEqual(res, 1.25)

    def test_get_variance_2(self):
        ds2 = DataStatistics2([1, 2, 203, 4])
        res = ds2.get_variance()
        self.assertEqual(res, 7551.25)

    def test_get_variance_3(self):
        ds2 = DataStatistics2([1, 4, 3, 2])
        res = ds2.get_variance()
        self.assertEqual(res, 1.25)

    def test_get_variance_4(self):
        ds2 = DataStatistics2([11, 14, 13, 12])
        res = ds2.get_variance()
        self.assertEqual(res, 1.25)

    def test_get_variance_5(self):
        ds2 = DataStatistics2([111, 114, 113, 112])
        res = ds2.get_variance()
        self.assertEqual(res, 1.25)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
