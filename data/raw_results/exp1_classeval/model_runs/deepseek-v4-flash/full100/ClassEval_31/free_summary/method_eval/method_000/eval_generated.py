import math

class DataStatistics4:
    @staticmethod
    def correlation_coefficient(data1, data2):
        n = len(data1)
        if n == 0:
            return 0

        mean1 = sum(data1) / n
        mean2 = sum(data2) / n

        covariance = sum((x - mean1) * (y - mean2) for x, y in zip(data1, data2))
        std1 = math.sqrt(sum((x - mean1) ** 2 for x in data1))
        std2 = math.sqrt(sum((y - mean2) ** 2 for y in data2))

        denominator = std1 * std2
        if denominator == 0:
            return 0

        return covariance / denominator

    @staticmethod
    def skewness(data):
        n = len(data)
        if n < 3:
            return 0

        mean = sum(data) / n
        m2 = sum((x - mean) ** 2 for x in data)
        if m2 == 0:
            return 0

        sample_std = math.sqrt(m2 / (n - 1))
        m3 = sum((x - mean) ** 3 for x in data)

        return (n / ((n - 1) * (n - 2))) * m3 / (sample_std ** 3)

    @staticmethod
    def kurtosis(data):
        n = len(data)
        if n == 0:
            return math.nan

        mean = sum(data) / n
        m2 = sum((x - mean) ** 2 for x in data)
        if m2 == 0:
            return math.nan

        variance = m2 / n
        m4 = sum((x - mean) ** 4 for x in data)
        fourth_moment = m4 / n

        return fourth_moment / (variance ** 2) - 3

    @staticmethod
    def pdf(data, mu, sigma):
        coefficient = 1.0 / (sigma * math.sqrt(2.0 * math.pi))
        return [
            coefficient * math.exp(-0.5 * ((x - mu) / sigma) ** 2)
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
