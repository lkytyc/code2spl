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
        if not data:
            raise ValueError("data must not be empty")
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        return sorted_data[mid]

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
            raise ValueError("data must not be empty")
        counts = {}
        for item in data:
            counts[item] = counts.get(item, 0) + 1
        max_count = max(counts.values())
        return [key for key, value in counts.items() if value == max_count]

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
        if not x or not y:
            raise ValueError("input lists must not be empty")
        if len(x) != len(y):
            raise ValueError("input lists must have the same length")

        mean_x = Statistics3.mean(x)
        mean_y = Statistics3.mean(y)

        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
        sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)

        denominator = math.sqrt(sum_sq_x * sum_sq_y)
        if denominator == 0:
            return 0.0
        return numerator / denominator

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
            raise ValueError("data must not be empty")
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
            raise ValueError("data must not be empty")
        matrix = []
        for i in range(len(data)):
            row = []
            for j in range(len(data)):
                row.append(Statistics3.correlation(data[i], data[j]))
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
            raise ValueError("data must not be empty")
        mean_value = Statistics3.mean(data)
        variance = sum((x - mean_value) ** 2 for x in data) / len(data)
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
            raise ValueError("data must not be empty")
        mean_value = Statistics3.mean(data)
        std_dev = Statistics3.standard_deviation(data)
        if std_dev == 0:
            return [0.0 for _ in data]
        return [(x - mean_value) / std_dev for x in data]

import unittest

class Statistics3TestMedian(unittest.TestCase):
    def test_median(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.median([1, 2, 3, 4]), 2.5)

    def test_median_2(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.median([1, 2, 3, 4, 5]), 3)

    def test_median_3(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.median([1, 2, 3, 4, 5, 6]), 3.5)

    def test_median_4(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.median([1, 2, 3, 4, 5, 6, 7]), 4)

    def test_median_5(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.median([1, 2, 3, 4, 5, 6, 7, 8]), 4.5)

class Statistics3TestMode(unittest.TestCase):
    def test_mode(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.mode([1, 2, 3, 3]), [3])

    def test_mode_2(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.mode([1, 2, 3, 3, 4, 4]), [3, 4])

    def test_mode_3(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.mode([1, 2, 3, 3, 4, 4, 5]), [3, 4])

    def test_mode_4(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.mode([1, 2, 3, 3, 4, 4, 5, 5]), [3, 4, 5])

    def test_mode_5(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.mode([1, 2, 3, 3, 4, 4, 5, 5, 6]), [3, 4, 5])

class Statistics3TestCorrelation(unittest.TestCase):
    def test_correlation(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.correlation([1, 2, 3], [4, 5, 6]), 1.0)

    def test_correlation_2(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.correlation([1, 2, 3, 4], [5, 6, 7, 8]), 1.0)

    def test_correlation_3(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.correlation([1, 2, 3], [1,2,3]), 1.0)

    def test_correlation_4(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.correlation([1, 1,1], [2,2,2]), None)

    def test_correlation_5(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.correlation([1, 1,1], [1,1,1]), None)

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

class Statistics3TestCorrelationMatrix(unittest.TestCase):
    def test_correlation_matrix(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.correlation_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]])

    def test_correlation_matrix_2(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.correlation_matrix([[1, 2, 3], [4, 5, 6]]), [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]])

    def test_correlation_matrix_3(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.correlation_matrix([[1, 2, 3]]), [[None, None, None], [None, None, None], [None, None, None]])

    def test_correlation_matrix_4(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.correlation_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11,12]]), [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]])

    def test_correlation_matrix_5(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.correlation_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11,12], [13, 14, 15]]), [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]])

class Statistics3TestStandardDeviation(unittest.TestCase):
    def test_standard_deviation(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.standard_deviation([1, 2, 3]), 1.0)

    def test_standard_deviation_2(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.standard_deviation([1, 1, 1]), 0.0)

    def test_standard_deviation_3(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.standard_deviation([1, 1]), 0.0)

    def test_standard_deviation_4(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.standard_deviation([1, 1, 1, 1]), 0.0)

    def test_standard_deviation_5(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.standard_deviation([1, 1, 2, 1, 4]), 1.3038404810405297)


class Statistics3TestZScore(unittest.TestCase):
    def test_z_score(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.z_score([1, 2, 3, 4]), [-1.161895003862225, -0.3872983346207417, 0.3872983346207417, 1.161895003862225])

    def test_z_score_2(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.z_score([1, 1, 1, 1]), None)

    def test_z_score_3(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.z_score([1]),None)

    def test_z_score_4(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.z_score([1, 1, 2, 3]), [-0.7833494518006403,-0.7833494518006403,0.26111648393354675,1.3055824196677337])

    def test_z_score_5(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.z_score([1, 1, 1, 1, 1]), None)


class Statistics3TestMain(unittest.TestCase):
    def test_main(self):
        statistics3 = Statistics3()
        self.assertEqual(statistics3.median([1, 2, 3, 4]), 2.5)
        self.assertEqual(statistics3.mode([1, 2, 3, 3]), [3])
        self.assertEqual(statistics3.correlation([1, 2, 3], [4, 5, 6]), 1.0)
        self.assertEqual(statistics3.mean([1, 2, 3]), 2.0)
        self.assertEqual(statistics3.correlation_matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), [[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]])
        self.assertEqual(statistics3.standard_deviation([1, 2, 3]), 1.0)
        self.assertEqual(statistics3.z_score([1, 2, 3, 4]), [-1.161895003862225, -0.3872983346207417, 0.3872983346207417, 1.161895003862225])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
