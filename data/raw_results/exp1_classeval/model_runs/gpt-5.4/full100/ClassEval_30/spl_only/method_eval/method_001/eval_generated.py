class DataStatistics2:
    def __init__(self, data):
        self.data = np.array(data)

    def get_sum(self):
        data = self.data
        sum_result = np.sum(data)
        return sum_result

    def get_min(self):
        data = self.data
        min_value = np.min(data)
        return min_value

    def get_max(self):
        try:
            data = self.data
            max_value = np.max(data)
            return max_value
        except Exception:
            raise ValueError("Raised when the input is empty or invalid for maximum computation.")

    def get_variance(self):
        data = self.data
        variance = np.var(data)
        return round(variance, 2)

    def get_std_deviation(self):
        std_value = np.std(self.data)
        rounded_std = round(std_value, 2)
        return rounded_std

    def get_correlation(self):
        data = self.data
        correlation_matrix = np.corrcoef(data, rowvar=False)
        return correlation_matrix

import unittest

class DataStatistics2TestGetMin(unittest.TestCase):
    def test_get_min_1(self):
        ds2 = DataStatistics2([1, 2, 3, 4])
        res = ds2.get_min()
        self.assertEqual(res, 1)

    def test_get_min_2(self):
        ds2 = DataStatistics2([1, 2, 203, 4])
        res = ds2.get_min()
        self.assertEqual(res, 1)

    def test_get_min_3(self):
        ds2 = DataStatistics2([0, -1, -3, 2])
        res = ds2.get_min()
        self.assertEqual(res, -3)

    def test_get_min_4(self):
        ds2 = DataStatistics2([-111, -1, -3, 2])
        res = ds2.get_min()
        self.assertEqual(res, -111)

    def test_get_min_5(self):
        ds2 = DataStatistics2([0, -1111, -3, 2])
        res = ds2.get_min()
        self.assertEqual(res, -1111)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
