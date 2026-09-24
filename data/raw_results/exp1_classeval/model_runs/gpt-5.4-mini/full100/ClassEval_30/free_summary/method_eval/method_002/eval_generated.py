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

class DataStatistics2TestGetMax(unittest.TestCase):
    def test_get_max_1(self):
        ds2 = DataStatistics2([1, 2, 3, 4])
        res = ds2.get_max()
        self.assertEqual(res, 4)

    def test_get_max_2(self):
        ds2 = DataStatistics2([1, 2, 203, 4])
        res = ds2.get_max()
        self.assertEqual(res, 203)

    def test_get_max_3(self):
        ds2 = DataStatistics2([-1, -4, 3, 2])
        res = ds2.get_max()
        self.assertEqual(res, 3)

    def test_get_max_4(self):
        ds2 = DataStatistics2([-1, 4, 3, 2])
        res = ds2.get_max()
        self.assertEqual(res, 4)

    def test_get_max_5(self):
        ds2 = DataStatistics2([-1, 444, 3, 2])
        res = ds2.get_max()
        self.assertEqual(res, 444)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
