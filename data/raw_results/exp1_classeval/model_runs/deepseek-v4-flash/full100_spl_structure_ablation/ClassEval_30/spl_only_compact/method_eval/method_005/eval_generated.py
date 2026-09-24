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

class DataStatistics2TestGetCorrelation(unittest.TestCase):
    def test_get_correlation_1(self):
        ds2 = DataStatistics2([1, 2, 3, 4])
        res = ds2.get_correlation()
        self.assertEqual(res, 1.0)

    def test_get_correlation_2(self):
        ds2 = DataStatistics2([1, 2, 203, 4])
        res = ds2.get_correlation()
        self.assertEqual(res, 1.0)

    def test_get_correlation_3(self):
        ds2 = DataStatistics2([1, 4, 3, 2])
        res = ds2.get_correlation()
        self.assertEqual(res, 1.0)

    def test_get_correlation_4(self):
        ds2 = DataStatistics2([11, 14, 13, 12])
        res = ds2.get_correlation()
        self.assertEqual(res, 1.0)

    def test_get_correlation_5(self):
        ds2 = DataStatistics2([111, 114, 113, 112])
        res = ds2.get_correlation()
        self.assertEqual(res, 1.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
