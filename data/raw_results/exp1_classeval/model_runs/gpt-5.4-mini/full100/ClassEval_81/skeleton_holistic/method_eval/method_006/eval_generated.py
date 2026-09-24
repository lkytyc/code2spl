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
        """
        if not data:
            return None
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 1:
            return sorted_data[mid]
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2

    @staticmethod
    def mode(data):
        """
        calculates the mode of the given list.
        :param data: the given list, list.
        :return: the mode of the given list, list.
        """
        if not data:
            return []
        counts = {}
        for item in data:
            counts[item] = counts.get(item, 0) + 1
        max_count = max(counts.values())
        return sorted([item for item, count in counts.items() if count == max_count])

    @staticmethod
    def correlation(x, y):
        """
        calculates the correlation of the given list.
        :param x: the given list, list.
        :param y: the given list, list.
        :return: the correlation of the given list, float.
        """
        if not x or not y or len(x) != len(y):
            return None
        mean_x = Statistics3.mean(x)
        mean_y = Statistics3.mean(y)
        numerator = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y))
        denom_x = sum((a - mean_x) ** 2 for a in x)
        denom_y = sum((b - mean_y) ** 2 for b in y)
        denominator = math.sqrt(denom_x * denom_y)
        if denominator == 0:
            return None
        return numerator / denominator

    @staticmethod
    def mean(data):
        """
        calculates the mean of the given list.
        :param data: the given list, list.
        :return: the mean of the given list, float.
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
        """
        if not data:
            return []
        n = len(data)
        matrix = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(Statistics3.correlation(data[i], data[j]))
            matrix.append(row)
        return matrix

    @staticmethod
    def standard_deviation(data):
        """
        calculates the standard deviation of the given list.
        :param data: the given list, list.
        :return: the standard deviation of the given list, float.
        """
        if not data:
            return None
        mean_val = Statistics3.mean(data)
        variance = sum((x - mean_val) ** 2 for x in data) / len(data)
        return math.sqrt(variance)

    @staticmethod
    def z_score(data):
        """
        calculates the z-score of the given list.
        :param data: the given list, list.
        :return: the z-score of the given list, list.
        """
        if not data:
            return []
        mean_val = Statistics3.mean(data)
        std = Statistics3.standard_deviation(data)
        if std == 0 or std is None:
            return [0 for _ in data]
        return [(x - mean_val) / std for x in data]

import unittest

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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
