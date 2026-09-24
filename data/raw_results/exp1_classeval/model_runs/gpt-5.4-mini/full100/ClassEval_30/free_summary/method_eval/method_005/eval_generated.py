import numpy as np

class DataStatistics2:
    def __init__(self, data):
        self.data = np.array(data)

    def total_sum(self):
        return np.sum(self.data)

    def minimum(self):
        return np.min(self.data)

    def maximum(self):
        return np.max(self.data)

    def variance(self):
        return round(float(np.var(self.data)), 2)

    def standard_deviation(self):
        return round(float(np.std(self.data)), 2)

    def correlation_matrix(self):
        return np.corrcoef(self.data, rowvar=False)

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
