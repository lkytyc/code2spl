import math


class DataStatistics4:

    @staticmethod
    def correlation_coefficient(data1, data2):
        n = len(data1)
        mean1 = sum(data1) / n
        mean2 = sum(data2) / n
        covariance = sum((data1[i] - mean1) * (data2[i] - mean2) for i in range(n)) / n
        std1 = math.sqrt(sum((x - mean1) ** 2 for x in data1) / n)
        std2 = math.sqrt(sum((x - mean2) ** 2 for x in data2) / n)
        denominator = std1 * std2
        if denominator == 0:
            return 0
        return covariance / denominator

    @staticmethod
    def skewness(data):
        n = len(data)
        mean = sum(data) / n
        std = math.sqrt(sum((x - mean) ** 2 for x in data) / n)
        if std == 0:
            return 0
        third_moment = sum((x - mean) ** 3 for x in data) / n
        return (n / ((n - 1) * (n - 2))) * (third_moment / std ** 3)

    @staticmethod
    def kurtosis(data):
        n = len(data)
        mean = sum(data) / n
        std = math.sqrt(sum((x - mean) ** 2 for x in data) / n)
        if std == 0:
            return math.nan
        fourth_moment = sum((x - mean) ** 4 for x in data) / n
        return (fourth_moment / std ** 4) - 3

    @staticmethod
    def pdf(data, mu, sigma):
        coefficient = 1 / (sigma * math.sqrt(2 * math.pi))
        return [coefficient * math.exp(-0.5 * ((x - mu) / sigma) ** 2) for x in data]

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
