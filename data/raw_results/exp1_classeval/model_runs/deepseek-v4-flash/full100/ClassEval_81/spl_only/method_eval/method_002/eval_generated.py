import math

class Statistics3:
    def median(self, data):
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 1:
            return sorted_data[n // 2]
        else:
            return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2

    def mode(self, data):
        counts = {}
        for value in data:
            counts[value] = counts.get(value, 0) + 1
        max_count = max(counts.values())
        mode_values = [value for value, count in counts.items() if count == max_count]
        return mode_values

    def correlation(self, x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) * sum((yi - mean_y) ** 2 for yi in y))
        if denominator == 0:
            return None
        return numerator / denominator

    def mean(self, data):
        if len(data) == 0:
            return None
        total = sum(data)
        count = len(data)
        mean_value = total / count
        return mean_value

    def correlation_matrix(self, data):
        matrix = []
        for i in range(len(data[0])):
            row = []
            for j in range(len(data[0])):
                column1 = [row_data[i] for row_data in data]
                column2 = [row_data[j] for row_data in data]
                correlation = self.correlation(column1, column2)
                row.append(correlation)
            matrix.append(row)
        return matrix

    def standard_deviation(self, data):
        n = len(data)
        if n < 2:
            return None
        mean_value = self.mean(data)
        variance = sum((x - mean_value) ** 2 for x in data) / (n - 1)
        return math.sqrt(variance)

    def z_score(self, data):
        mean = self.mean(data)
        std_deviation = self.standard_deviation(data)
        if std_deviation is None or std_deviation == 0:
            return None
        return [(x - mean) / std_deviation for x in data]

import unittest

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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
