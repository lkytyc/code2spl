class DataStatistics2:
    def __init__(self, data):
        import numpy as np

        array_data = np.array(data)
        self.data = array_data

    def get_correlation(self):
        import numpy as np

        data = self.data
        correlation_matrix = np.corrcoef(data, rowvar=False)
        return correlation_matrix

    def get_max(self):
        import logging
        import numpy as np

        data = self.data
        try:
            max_value = np.max(data)
        except ValueError:
            logging.getLogger(__name__).error(
                "np.max(self.data) cannot determine a maximum for the provided data."
            )
            raise
        return max_value

    def get_min(self):
        import numpy as np

        data = self.data
        min_value = np.min(data)
        return min_value

    def get_std_deviation(self):
        import numpy as np

        std_value = np.std(self.data)
        rounded_std = round(std_value, 2)
        return rounded_std

    def get_sum(self):
        import numpy as np

        data = self.data
        sum_result = np.sum(data)
        return sum_result

    def get_variance(self):
        import numpy as np

        data = self.data
        variance = np.var(data)
        return round(variance, 2)

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


class DataStatistics2Test(unittest.TestCase):
    def test_datastatistics2(self):
        ds2 = DataStatistics2([1, 2, 3, 4])
        res = ds2.get_sum()
        self.assertEqual(res, 10)

        res = ds2.get_min()
        self.assertEqual(res, 1)

        res = ds2.get_max()
        self.assertEqual(res, 4)

        res = ds2.get_variance()
        self.assertEqual(res, 1.25)

        res = ds2.get_std_deviation()
        self.assertEqual(res, 1.12)

        res = ds2.get_correlation()
        self.assertEqual(res, 1.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
