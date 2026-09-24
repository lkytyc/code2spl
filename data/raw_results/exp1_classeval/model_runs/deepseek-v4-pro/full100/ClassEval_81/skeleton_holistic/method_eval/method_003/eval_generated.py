import math

class Statistics3:
    """
    This is a class that implements methods for calculating indicators such as median, mode, correlation matrix, and Z-score in statistics.
    """

    @staticmethod
    def median(data):
        """
        calculates the median of the given list.
        :param data: the given list, list.
        :return: the median of the given list, float.
        >>> statistics3 = Statistics3()
        >>> statistics3.median([1, 2, 3, 4])
        2.5

        """
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n == 0:
            return None
        mid = n // 2
        if n % 2 == 1:
            return float(sorted_data[mid])
        else:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2.0

    @staticmethod
    def mode(data):
        """
        calculates the mode of the given list.
        :param data: the given list, list.
        :return: the mode of the given list, list.
        >>> statistics3 = Statistics3()
        >>> statistics3.mode([1, 2, 3, 3])
        [3]

        """
        if not data:
            return []
        freq = {}
        for item in data:
            freq[item] = freq.get(item, 0) + 1
        max_count = max(freq.values())
        modes = [key for key, count in freq.items() if count == max_count]
        return modes

    @staticmethod
    def correlation(x, y):
        """
        calculates the correlation of the given list.
        :param x: the given list, list.
        :param y: the given list, list.
        :return: the correlation of the given list, float.
        >>> statistics3 = Statistics3()
        >>> statistics3.correlation([1, 2, 3], [4, 5, 6])
        1.0

        """
        if len(x) != len(y) or len(x) == 0:
            return None
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        if std_x == 0 or std_y == 0:
            return None
        return cov / (std_x * std_y)

    @staticmethod
    def mean(data):
        """
        calculates the mean of the given list.
        :param data: the given list, list.
        :return: the mean of the given list, float.
        >>> statistics3 = Statistics3()
        >>> statistics3.mean([1, 2, 3])
        2.0

        """
        if not data:
            return None
        return sum(data) / len(data)

    @staticmethod
    def correlation_matrix(data):
        """
        calculates the correlation matrix of the given list.
        :param data: the given list, list.
        :return: the correlation matrix of the given list, list.
        >>> statistics3 = Statistics3()
        >>> statistics3.correlation_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]

        """
        if not data:
            return []
        n = len(data)
        matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                corr = Statistics3.correlation(data[i], data[j])
                row.append(corr if corr is not None else 0.0)
            matrix.append(row)
        return matrix

    @staticmethod
    def standard_deviation(data):
        """
        calculates the standard deviation of the given list.
        :param data: the given list, list.
        :return: the standard deviation of the given list, float.
        >>> statistics3 = Statistics3()
        >>> statistics3.standard_deviation([1, 2, 3])
        1.0

        """
        if not data:
            return None
        mean = Statistics3.mean(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        return math.sqrt(variance)

    @staticmethod
    def z_score(data):
        """
        calculates the z-score of the given list.
        :param data: the given list, list.
        :return: the z-score of the given list, list.
        >>> statistics3 = Statistics3()
        >>> statistics3.z_score([1, 2, 3, 4])
        [-1.161895003862225, -0.3872983346207417, 0.3872983346207417, 1.161895003862225]

        """
        if not data:
            return []
        mean = Statistics3.mean(data)
        std = Statistics3.standard_deviation(data)
        if std == 0:
            return [0.0] * len(data)
        return [(x - mean) / std for x in data]

import unittest

class Statistics3TestMean(unittest.TestCase):
    def test_mean(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.mean([1, 2, 3]), 2.0)

    def test_mean_2(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.mean([]), None)

    def test_mean_3(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.mean([1, 1, 1]), 1.0)

    def test_mean_4(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.mean([1, 1, 1, 1]), 1.0)

    def test_mean_5(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.mean([1, 1, 1, 1, 1]), 1.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
