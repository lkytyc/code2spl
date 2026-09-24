class Statistics3:
    @staticmethod
    def median(data):
        values = sorted(data)
        n = len(values)
        if n == 0:
            return None
        mid = n // 2
        if n % 2 == 1:
            return values[mid]
        return (values[mid - 1] + values[mid]) / 2

    @staticmethod
    def mode(data):
        counts = {}
        for value in data:
            counts[value] = counts.get(value, 0) + 1
        if not counts:
            return []
        max_count = max(counts.values())
        return [value for value, count in counts.items() if count == max_count]

    @staticmethod
    def mean(data):
        values = list(data)
        if not values:
            return None
        return sum(values) / len(values)

    @staticmethod
    def standard_deviation(data):
        values = list(data)
        n = len(values)
        if n < 2:
            return None
        mean_value = Statistics3.mean(values)
        variance = sum((x - mean_value) ** 2 for x in values) / (n - 1)
        return math.sqrt(variance)

    @staticmethod
    def z_score(data):
        values = list(data)
        mean_value = Statistics3.mean(values)
        std_dev = Statistics3.standard_deviation(values)
        if std_dev is None or std_dev == 0:
            return None
        return [(x - mean_value) / std_dev for x in values]

    @staticmethod
    def correlation(x, y):
        x_values = list(x)
        y_values = list(y)
        if len(x_values) != len(y_values) or len(x_values) == 0:
            return None

        x_mean = Statistics3.mean(x_values)
        y_mean = Statistics3.mean(y_values)
        x_std = Statistics3.standard_deviation(x_values)
        y_std = Statistics3.standard_deviation(y_values)

        if x_std is None or y_std is None or x_std == 0 or y_std == 0:
            return None

        numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x_values, y_values))
        denominator = (len(x_values) - 1) * x_std * y_std
        if denominator == 0:
            return None
        return numerator / denominator

    @staticmethod
    def correlation_matrix(data):
        rows = [list(row) for row in data]
        if not rows:
            return []
        num_columns = len(rows[0])
        columns = []
        for col_index in range(num_columns):
            columns.append([row[col_index] for row in rows])

        matrix = []
        for i in range(num_columns):
            row = []
            for j in range(num_columns):
                row.append(Statistics3.correlation(columns[i], columns[j]))
            matrix.append(row)
        return matrix

import math

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
