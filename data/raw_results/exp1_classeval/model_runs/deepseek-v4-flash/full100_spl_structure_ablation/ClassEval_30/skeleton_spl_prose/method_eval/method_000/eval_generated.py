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
        return np.sum(self.data)

    def get_min(self):
        """
        Calculate the minimum value in the data
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_min()
        1
        """
        return np.min(self.data)

    def get_max(self):
        """
        Calculate the maximum value in the data
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_max()
        4
        """
        return np.max(self.data)

    def get_variance(self):
        """
        Calculate variance, accurate to two digits after the Decimal separator
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_variance()
        1.25
        """
        variance = np.var(self.data)
        return round(variance, 2)

    def get_std_deviation(self):
        """
        Calculate standard deviation, accurate to two digits after the Decimal separator
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_std_deviation()
        1.12
        """
        std_dev = np.std(self.data)
        return round(std_dev, 2)

    def get_correlation(self):
        """
        Calculate correlation
        :return:float
        >>> ds2 = DataStatistics2([1, 2, 3, 4])
        >>> ds2.get_correlation()
        1.0
        """
        return np.corrcoef(self.data, rowvar=False)

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
