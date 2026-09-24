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
