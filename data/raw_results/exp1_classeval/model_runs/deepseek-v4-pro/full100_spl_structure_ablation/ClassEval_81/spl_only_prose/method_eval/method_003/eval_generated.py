import math
from typing import Collection, List, Sequence, Union, Optional, Any


class Statistics3:

    @staticmethod
    def correlation(x: Sequence[float], y: Sequence[float]) -> Optional[float]:
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(
            sum((xi - mean_x) ** 2 for xi in x) *
            sum((yi - mean_y) ** 2 for yi in y)
        )
        if denominator != 0:
            return numerator / denominator
        return None

    @staticmethod
    def correlation_matrix(data: List[List[float]]) -> List[List[float]]:
        matrix = []
        n = len(data[0])
        for i in range(n):
            row = []
            for j in range(n):
                column1 = [row[i] for row in data]
                column2 = [row[j] for row in data]
                correlation = Statistics3.correlation(column1, column2)
                row.append(correlation)
            matrix.append(row)
        return matrix

    @staticmethod
    def mean(data: Collection[float]) -> Optional[float]:
        data_length = len(data)
        if data_length != 0:
            mean_result = sum(data) / data_length
            return mean_result
        return None

    @staticmethod
    def median(data: Sequence[float]) -> float:
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 1:
            median_result = sorted_data[n // 2]
            return median_result
        median_result = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
        return median_result

    @staticmethod
    def mode(data: List[Any]) -> List[Any]:
        counts = {}
        for value in data:
            counts[value] = counts.get(value, 0) + 1
        max_count = max(counts.values())
        mode_values = [value for value, count in counts.items() if count == max_count]
        return mode_values

    @staticmethod
    def standard_deviation(data: Sequence[float]) -> Optional[float]:
        n = len(data)
        if n < 2:
            return None
        mean_value = Statistics3.mean(data)
        variance = sum((x - mean_value) ** 2 for x in data) / (n - 1)
        return_value = math.sqrt(variance)
        return return_value

    @staticmethod
    def z_score(data: List[float]) -> Optional[List[float]]:
        mean = Statistics3.mean(data)
        std_deviation = Statistics3.standard_deviation(data)
        if std_deviation is not None and std_deviation != 0:
            z_scores = [(x - mean) / std_deviation for x in data]
            return z_scores
        return None

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
