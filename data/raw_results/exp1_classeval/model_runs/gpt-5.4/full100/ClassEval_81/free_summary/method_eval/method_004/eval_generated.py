import math


class Statistics3:
    @staticmethod
    def mean(data):
        if not data:
            return None
        return sum(data) / len(data)

    @staticmethod
    def median(data):
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
        if not data:
            return []
        counts = {}
        for value in data:
            counts[value] = counts.get(value, 0) + 1
        max_count = max(counts.values())
        return [value for value, count in counts.items() if count == max_count]

    @staticmethod
    def correlation(x, y):
        if len(x) != len(y) or len(x) == 0:
            return None

        mean_x = Statistics3.mean(x)
        mean_y = Statistics3.mean(y)

        numerator = sum((a - mean_x) * (b - mean_y) for a, b in zip(x, y))
        sum_sq_x = sum((a - mean_x) ** 2 for a in x)
        sum_sq_y = sum((b - mean_y) ** 2 for b in y)

        denominator = math.sqrt(sum_sq_x * sum_sq_y)
        if denominator == 0:
            return None

        return numerator / denominator

    @staticmethod
    def correlation_matrix(data):
        if not data or not data[0]:
            return []

        num_columns = len(data[0])
        columns = [[row[i] for row in data] for i in range(num_columns)]

        matrix = []
        for i in range(num_columns):
            row = []
            for j in range(num_columns):
                row.append(Statistics3.correlation(columns[i], columns[j]))
            matrix.append(row)
        return matrix

    @staticmethod
    def standard_deviation(data):
        if len(data) < 2:
            return None
        mean_value = Statistics3.mean(data)
        variance = sum((x - mean_value) ** 2 for x in data) / (len(data) - 1)
        return math.sqrt(variance)

    @staticmethod
    def z_score(data):
        if not data:
            return None
        mean_value = Statistics3.mean(data)
        std_dev = Statistics3.standard_deviation(data)
        if std_dev is None or std_dev == 0:
            return None
        return [(x - mean_value) / std_dev for x in data]

import unittest

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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
