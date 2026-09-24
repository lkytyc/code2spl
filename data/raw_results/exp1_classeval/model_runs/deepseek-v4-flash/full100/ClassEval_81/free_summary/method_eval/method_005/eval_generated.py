class Statistics3:
    @staticmethod
    def median(data):
        if not data:
            return None
        sorted_data = sorted(data)
        n = len(sorted_data)
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
        for item in data:
            freq[item] = freq.get(item, 0) + 1
        max_freq = max(freq.values())
        return [key for key, value in freq.items() if value == max_freq]

    @staticmethod
    def mean(data):
        if not data:
            return None
        return sum(data) / len(data)

    @staticmethod
    def pearson_correlation(x, y):
        n = len(x)
        if n != len(y) or n == 0:
            return None
        mean_x = Statistics3.mean(x)
        mean_y = Statistics3.mean(y)
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = (sum((xi - mean_x) ** 2 for xi in x) * sum((yi - mean_y) ** 2 for yi in y)) ** 0.5
        if denominator == 0:
            return None
        return numerator / denominator

    @staticmethod
    def correlation_matrix(dataset):
        if not dataset or not dataset[0]:
            return []
        num_cols = len(dataset[0])
        matrix = [[None] * num_cols for _ in range(num_cols)]
        for i in range(num_cols):
            for j in range(num_cols):
                col_i = [row[i] for row in dataset]
                col_j = [row[j] for row in dataset]
                matrix[i][j] = Statistics3.pearson_correlation(col_i, col_j)
        return matrix

    @staticmethod
    def sample_standard_deviation(data):
        if len(data) < 2:
            return None
        mean = Statistics3.mean(data)
        variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
        return variance ** 0.5

    @staticmethod
    def z_scores(data):
        mean = Statistics3.mean(data)
        std = Statistics3.sample_standard_deviation(data)
        if std is None or std == 0:
            return None
        return [(x - mean) / std for x in data]

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
