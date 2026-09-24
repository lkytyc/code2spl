class DataStatistics4:
    def correlation_coefficient(self, data1, data2):
        n = len(data1)
        mean1 = sum(data1) / n
        mean2 = sum(data2) / n
        numerator = sum((data1[i] - mean1) * (data2[i] - mean2) for i in range(n))
        data1_scale = sum((data1[i] - mean1) ** 2 for i in range(n)) ** 0.5
        data2_scale = sum((data2[i] - mean2) ** 2 for i in range(n)) ** 0.5
        denominator = data1_scale * data2_scale
        if denominator != 0:
            return numerator / denominator
        return 0

    def skewness(self, data):
        n = len(data)
        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / n
        std_deviation = variance ** 0.5
        if std_deviation != 0:
            skewness = sum((x - mean) ** 3 for x in data) * n / ((n - 1) * (n - 2) * (std_deviation ** 3))
        else:
            skewness = 0
        return skewness

    def kurtosis(self, data):
        n = len(data)
        mean = sum(data) / n
        std_dev = (sum((x - mean) ** 2 for x in data) / n) ** 0.5
        if std_dev == 0:
            return math.nan
        centered_data = [x - mean for x in data]
        fourth_moment = sum(x ** 4 for x in centered_data) / n
        kurtosis_value = (fourth_moment / (std_dev ** 4)) - 3
        return kurtosis_value

    def pdf(self, data, mu, sigma):
        return [1 / (sigma * math.sqrt(2 * math.pi)) * math.exp(-0.5 * ((x - mu) / sigma) ** 2) for x in data]

import unittest

class DataStatistics4TestKurtosis(unittest.TestCase):
    def test_kurtosis(self):
        self.assertEqual(DataStatistics4.kurtosis([1, 2, 5]), -1.5000000000000002)

    def test_kurtosis_2(self):
        self.assertTrue(math.isnan(DataStatistics4.kurtosis([1, 1, 1])))

    def test_kurtosis_3(self):
        self.assertEqual(DataStatistics4.kurtosis([1, 2, 3]), -1.5000000000000002)

    def test_kurtosis_4(self):
        self.assertEqual(DataStatistics4.kurtosis([1, 2, 4]), -1.4999999999999996)

    def test_kurtosis_5(self):
        self.assertEqual(DataStatistics4.kurtosis([1, 5, 3]), -1.5000000000000002)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
