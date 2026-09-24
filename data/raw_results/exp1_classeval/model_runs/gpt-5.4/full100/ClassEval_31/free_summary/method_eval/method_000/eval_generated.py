import math


class DataStatistics4:
    @staticmethod
    def correlation_coefficient(data1, data2):
        if len(data1) != len(data2) or len(data1) == 0:
            return 0

        mean1 = sum(data1) / len(data1)
        mean2 = sum(data2) / len(data2)

        numerator = sum((x - mean1) * (y - mean2) for x, y in zip(data1, data2))
        denom1 = sum((x - mean1) ** 2 for x in data1)
        denom2 = sum((y - mean2) ** 2 for y in data2)
        denominator = math.sqrt(denom1 * denom2)

        if denominator == 0:
            return 0

        return numerator / denominator

    @staticmethod
    def skewness(data):
        n = len(data)
        if n == 0:
            return 0

        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / n
        std_dev = math.sqrt(variance)

        if std_dev == 0:
            return 0

        third_moment = sum((x - mean) ** 3 for x in data) / n
        return third_moment / (std_dev ** 3)

    @staticmethod
    def kurtosis(data):
        n = len(data)
        if n == 0:
            return math.nan

        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / n
        std_dev = math.sqrt(variance)

        if std_dev == 0:
            return math.nan

        fourth_moment = sum((x - mean) ** 4 for x in data) / n
        return fourth_moment / (std_dev ** 4) - 3

    @staticmethod
    def pdf(data, mu, sigma):
        if sigma == 0:
            return [0 for _ in data]

        coefficient = 1 / (sigma * math.sqrt(2 * math.pi))
        return [
            coefficient * math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
            for x in data
        ]

import unittest

class DataStatistics4TestCorrelationCoefficient(unittest.TestCase):
    def test_correlation_coefficient(self):
        self.assertEqual(DataStatistics4.correlation_coefficient([1, 2, 3], [4, 5, 6]), 0.9999999999999998)

    def test_correlation_coefficient_2(self):
        self.assertEqual(DataStatistics4.correlation_coefficient([1, 1, 1], [2, 2, 2]), 0)

    def test_correlation_coefficient_3(self):
        self.assertEqual(DataStatistics4.correlation_coefficient([1, 2, 3], [1, 2, 3]), 0.9999999999999998)

    def test_correlation_coefficient_4(self):
        self.assertEqual(DataStatistics4.correlation_coefficient([1, 2, 3], [1, 2, 4]), 0.9819805060619659)

    def test_correlation_coefficient_5(self):
        self.assertEqual(DataStatistics4.correlation_coefficient([1, 2, 3], [1, 5, 3]), 0.4999999999999999)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
