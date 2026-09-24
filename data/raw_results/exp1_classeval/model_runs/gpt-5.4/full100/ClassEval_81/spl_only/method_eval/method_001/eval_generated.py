class Statistics3:
    def mean(self, data):
        if len(data) == 0:
            return None
        return sum(data) / len(data)

    def median(self, data):
        sorted_data = sorted(data)
        n = len(sorted_data)
        if n % 2 == 1:
            return sorted_data[n // 2]
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2

    def mode(self, data):
        counts = {}
        for value in data:
            counts[value] = counts.get(value, 0) + 1
        if not counts:
            raise ValueError("Raised when attempting to compute the maximum frequency from an empty collection.")
        max_count = max(counts.values())
        mode_values = [value for value, count in counts.items() if count == max_count]
        return mode_values

    def standard_deviation(self, data):
        n = len(data)
        if n < 2:
            return None
        mean_value = self.mean(data)
        variance = sum((x - mean_value) ** 2 for x in data) / (n - 1)
        return __import__("math").sqrt(variance)

    def z_score(self, data):
        mean = self.mean(data)
        std_deviation = self.standard_deviation(data)
        if std_deviation is None or std_deviation == 0:
            return None
        return [(x - mean) / std_deviation for x in data]

    def correlation(self, x, y):
        import math
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = math.sqrt(
            sum((xi - mean_x) ** 2 for xi in x) *
            sum((yi - mean_y) ** 2 for yi in y)
        )
        if denominator == 0:
            return None
        return numerator / denominator

    def correlation_matrix(self, data):
        matrix = []
        for i in range(len(data[0])):
            row = []
            for j in range(len(data[0])):
                column1 = [r[i] for r in data]
                column2 = [r[j] for r in data]
                correlation = self.correlation(column1, column2)
                row.append(correlation)
            matrix.append(row)
        return matrix

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
