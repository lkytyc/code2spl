import math

class Statistics3:
    @staticmethod
    def median(data):
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n == 0:
            return None
        mid = n // 2
        if n % 2 == 1:
            return sorted_data[mid]
        else:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2

    @staticmethod
    def mode(data):
        if not data:
            return []
        freq = {}
        for value in data:
            freq[value] = freq.get(value, 0) + 1
        max_count = max(freq.values())
        return [key for key, count in freq.items() if count == max_count]

    @staticmethod
    def correlation(x, y):
        if len(x) != len(y) or len(x) == 0:
            return None
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
        sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)
        denominator = math.sqrt(sum_sq_x * sum_sq_y)
        if denominator == 0:
            return None
        return numerator / denominator

    @staticmethod
    def mean(data):
        if not data:
            return None
        return sum(data) / len(data)

    @staticmethod
    def correlation_matrix(data):
        if not data:
            return []
        num_cols = len(data[0])
        matrix = [[0.0] * num_cols for _ in range(num_cols)]
        for i in range(num_cols):
            for j in range(num_cols):
                col_i = [row[i] for row in data]
                col_j = [row[j] for row in data]
                matrix[i][j] = Statistics3.correlation(col_i, col_j)
        return matrix

    @staticmethod
    def standard_deviation(data):
        if len(data) < 2:
            return None
        mean_val = sum(data) / len(data)
        variance = sum((x - mean_val) ** 2 for x in data) / (len(data) - 1)
        return math.sqrt(variance)

    @staticmethod
    def z_score(data):
        if len(data) < 2:
            return None
        mean_val = sum(data) / len(data)
        std_dev = Statistics3.standard_deviation(data)
        if std_dev is None or std_dev == 0:
            return None
        return [(x - mean_val) / std_dev for x in data]

import unittest

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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
