import math


class DataStatistics4:
    def correlation_coefficient(self, data1, data2):
        n = len(data1)
        mean1 = sum(data1) / n
        mean2 = sum(data2) / n
        numerator = 0
        for i in range(n):
            numerator += (data1[i] - mean1) * (data2[i] - mean2)
        data1_scale = math.sqrt(sum((data1[i] - mean1) ** 2 for i in range(n)))
        data2_scale = math.sqrt(sum((data2[i] - mean2) ** 2 for i in range(n)))
        denominator = data1_scale * data2_scale
        if denominator != 0:
            return numerator / denominator
        return 0

    def kurtosis(self, data):
        n = len(data)
        mean = sum(data) / n
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in data) / n)
        if std_dev == 0:
            return math.nan
        centered_data = [x - mean for x in data]
        fourth_moment = sum(x ** 4 for x in centered_data) / n
        kurtosis_value = (fourth_moment / (std_dev ** 4)) - 3
        return kurtosis_value

    def pdf(self, data, mu, sigma):
        pdf_values = [
            (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * (((x - mu) / sigma) ** 2))
            for x in data
        ]
        return pdf_values

    def skewness(self, data):
        n = len(data)
        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / n
        std_deviation = math.sqrt(variance)
        if std_deviation != 0:
            skewness = (
                sum((x - mean) ** 3 for x in data) * n
                / ((n - 1) * (n - 2) * (std_deviation ** 3))
            )
        else:
            skewness = 0
        return skewness

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
