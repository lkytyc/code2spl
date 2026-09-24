import numpy as np

class DataStatistics2:
    def __init__(self, data):
        self.data = np.array(data)

    def get_sum(self):
        return float(np.sum(self.data))

    def get_min(self):
        return float(np.min(self.data))

    def get_max(self):
        return float(np.max(self.data))

    def get_variance(self):
        return round(float(np.var(self.data)), 2)

    def get_std_deviation(self):
        return round(float(np.std(self.data)), 2)

    def get_correlation(self):
        return float(np.corrcoef(self.data, self.data)[0, 1])

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
