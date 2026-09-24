import math
from collections import Counter
from typing import Optional


class Statistics3:

    @staticmethod
    def mean(data: list) -> Optional[float]:
        if not data:
            return None
        return sum(data) / len(data)

    @staticmethod
    def median(data: list) -> Optional[float]:
        if not data:
            return None
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 1:
            return sorted_data[mid]
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2

    @staticmethod
    def mode(data: list) -> list:
        if not data:
            return []
        counts = Counter(data)
        max_count = max(counts.values())
        return [value for value, count in counts.items() if count == max_count]

    @staticmethod
    def standard_deviation(data: list) -> Optional[float]:
        if len(data) < 2:
            return None
        m = Statistics3.mean(data)
        variance = sum((x - m) ** 2 for x in data) / (len(data) - 1)
        return math.sqrt(variance)

    @staticmethod
    def z_score(data: list) -> Optional[list]:
        if len(data) < 2:
            return None
        sd = Statistics3.standard_deviation(data)
        if sd is None or sd == 0:
            return None
        m = Statistics3.mean(data)
        return [(x - m) / sd for x in data]

    @staticmethod
    def correlation(x: list, y: list) -> Optional[float]:
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denom_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)))
        denom_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))
        denominator = denom_x * denom_y
        if denominator == 0:
            return None
        return numerator / denominator

    @staticmethod
    def correlation_matrix(data: list) -> list:
        if not data:
            return []
        num_vars = len(data[0])
        columns = [[row[j] for row in data] for j in range(num_vars)]
        return [
            [Statistics3.correlation(columns[i], columns[j]) for j in range(num_vars)]
            for i in range(num_vars)
        ]

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
