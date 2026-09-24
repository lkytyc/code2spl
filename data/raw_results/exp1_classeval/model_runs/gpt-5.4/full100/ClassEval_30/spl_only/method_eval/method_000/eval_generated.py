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
