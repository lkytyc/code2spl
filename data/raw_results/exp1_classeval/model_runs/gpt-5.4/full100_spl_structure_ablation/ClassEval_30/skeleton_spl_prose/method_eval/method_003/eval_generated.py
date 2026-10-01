import numpy as np


class DataStatistics2:
    """
    This is a class for performing data statistics, supporting to get the sum, minimum, maximum, variance, standard deviation, and correlation of a given dataset.
    """

    def __init__(self, data):
        """
        Initialize Data List
        :param data:list
        """
        self.data = np.array(data)

    def get_sum(self):
        """
        Calculate the sum of data
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_sum()
        10
        """
        data = self.data
        sum_result = np.sum(data)
        return sum_result

    def get_min(self):
        """
        Calculate the minimum value in the data
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_min()
        1
        """
        data = self.data
        min_value = np.min(data)
        return min_value

    def get_max(self):
        """
        Calculate the maximum value in the data
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_max()
        4
        """
        data = self.data
        max_value = np.max(data)
        return max_value

    def get_variance(self):
        """
        Calculate variance, accurate to two digits after the Decimal separator
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_variance()
        1.25
        """
        data = self.data
        variance = np.var(data)
        result = round(variance, 2)
        return result

    def get_std_deviation(self):
        """
        Calculate standard deviation, accurate to two digits after the Decimal separator
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_std_deviation()
        1.12
        """
        std_value = np.std(self.data)
        rounded_std = round(std_value, 2)
        return rounded_std

    def get_correlation(self):
        """
        Calculate correlation
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_correlation()
        1.0
        """
        data = self.data
        correlation_matrix = np.corrcoef(data, rowvar=False)
        return correlation_matrix

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
