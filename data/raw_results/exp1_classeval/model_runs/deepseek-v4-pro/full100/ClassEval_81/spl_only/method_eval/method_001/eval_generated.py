import math


class Statistics3:
    @staticmethod
    def median(data):
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 1:
            median_result = sorted_data[n // 2]
            return median_result
        else:
            median_result = (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
            return median_result

    @staticmethod
    def mode(data):
        counts = {}
        for value in data:
            counts[value] = counts.get(value, 0) + 1
        max_count = max(counts.values())
        mode_values = [value for value, count in counts.items() if count == max_count]
        return mode_values

    @staticmethod
    def correlation(x, y):
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
        else:
            return None

    @staticmethod
    def mean(data):
        data_length = len(data)
        if data_length != 0:
            mean_result = sum(data) / len(data)
            return mean_result
        else:
            return None

    @staticmethod
    def correlation_matrix(data):
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
    def standard_deviation(data):
        n = len(data)
        if n < 2:
            return None
        mean_value = Statistics3.mean(data)
        variance = sum((x - mean_value) ** 2 for x in data) / (n - 1)
        return math.sqrt(variance)

    @staticmethod
    def z_score(data):
        mean = Statistics3.mean(data)
        std_deviation = Statistics3.standard_deviation(data)
        if std_deviation is not None and std_deviation != 0:
            z_scores = [(x - mean) / std_deviation for x in data]
            return z_scores
        else:
            return None

import unittest

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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
