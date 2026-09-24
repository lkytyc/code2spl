import numpy as np

class DataStatistics2:
    def __init__(self, data):
        numpy_array = np.array(data)
        self.data = numpy_array

    def get_correlation(self):
        result = np.corrcoef(self.data, rowvar=False)
        return result

    def get_max(self):
        data_array = self.data
        max_value = np.max(data_array)
        return max_value

    def get_min(self):
        data = self.data
        min_value = np.min(data)
        return min_value

    def get_std_deviation(self):
        std_dev = np.std(self.data)
        rounded_std_dev = round(std_dev, 2)
        return rounded_std_dev

    def get_sum(self):
        return np.sum(self.data)

    def get_variance(self):
        data = self.data
        variance = np.var(data)
        rounded_variance = round(variance, 2)
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
