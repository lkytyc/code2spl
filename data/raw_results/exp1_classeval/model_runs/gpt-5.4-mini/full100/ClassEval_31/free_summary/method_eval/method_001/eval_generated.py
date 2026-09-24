import math


class DataStatistics4:
    @staticmethod
    def correlation_coefficient(data1, data2):
        n = len(data1)
        if n != len(data2) or n == 0:
            return 0

        mean1 = sum(data1) / n
        mean2 = sum(data2) / n

        numerator = 0
        denom1 = 0
        denom2 = 0
        for x, y in zip(data1, data2):
            dx = x - mean1
            dy = y - mean2
            numerator += dx * dy
            denom1 += dx * dx
            denom2 += dy * dy

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
        m2 = 0
        m3 = 0
        for x in data:
            d = x - mean
            d2 = d * d
            m2 += d2
            m3 += d2 * d

        variance = m2 / n
        stddev = math.sqrt(variance)
        if stddev == 0:
            return 0

        return (m3 / n) / (stddev ** 3)

    @staticmethod
    def kurtosis(data):
        n = len(data)
        if n == 0:
            return math.nan

        mean = sum(data) / n
        m2 = 0
        m4 = 0
        for x in data:
            d = x - mean
            d2 = d * d
            m2 += d2
            m4 += d2 * d2

        variance = m2 / n
        stddev = math.sqrt(variance)
        if stddev == 0:
            return math.nan

        return (m4 / n) / (stddev ** 4) - 3

    @staticmethod
    def pdf(data, mu, sigma):
        if sigma == 0:
            return [math.nan for _ in data]

        coeff = 1.0 / (sigma * math.sqrt(2.0 * math.pi))
        return [coeff * math.exp(-((x - mu) ** 2) / (2.0 * sigma * sigma)) for x in data]

import unittest

class DataStatistics4TestSkewness(unittest.TestCase):
    def test_skewness(self):
        self.assertEqual(DataStatistics4.skewness([1, 2, 5]), 2.3760224064818463)

    def test_skewness_2(self):
        self.assertEqual(DataStatistics4.skewness([1, 1, 1]), 0)

    def test_skewness_3(self):
        self.assertEqual(DataStatistics4.skewness([1, 2, 3]), 0)

    def test_skewness_4(self):
        self.assertEqual(DataStatistics4.skewness([1, 2, 4]), 1.7181079837227264)

    def test_skewness_5(self):
        self.assertEqual(DataStatistics4.skewness([1, 5, 3]), 0.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
