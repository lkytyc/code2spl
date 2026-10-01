class DataStatistics4:
    import math

    def correlation_coefficient(self, data1, data2):
        n = len(data1)
        mean1 = sum(data1) / n
        mean2 = sum(data2) / n

        numerator = sum(
            (data1[i] - mean1) * (data2[i] - mean2)
            for i in range(n)
        )
        denominator = (
            self.math.sqrt(
                sum((data1[i] - mean1) ** 2 for i in range(n))
            )
            * self.math.sqrt(
                sum((data2[i] - mean2) ** 2 for i in range(n))
            )
        )

        if denominator != 0:
            return numerator / denominator
        return 0

    def kurtosis(self, data):
        n = len(data)
        mean = sum(data) / n
        std_dev = self.math.sqrt(
            sum((value - mean) ** 2 for value in data) / n
        )

        if std_dev == 0:
            return self.math.nan

        centered_data = [value - mean for value in data]
        fourth_moment = sum(value ** 4 for value in centered_data) / n
        kurtosis_value = fourth_moment / (std_dev ** 4) - 3
        return kurtosis_value

    def pdf(self, data, mu, sigma):
        pdf_values = [
            1 / (sigma * self.math.sqrt(2 * self.math.pi))
            * self.math.exp(-0.5 * ((x - mu) / sigma) ** 2)
            for x in data
        ]
        return pdf_values

    def skewness(self, data):
        n = len(data)
        mean = sum(data) / n
        variance = sum((value - mean) ** 2 for value in data) / n
        std_deviation = self.math.sqrt(variance)

        if std_deviation != 0:
            skewness = (
                sum((value - mean) ** 3 for value in data)
                * n
                / ((n - 1) * (n - 2) * std_deviation ** 3)
            )
        else:
            skewness = 0

        return skewness

import unittest

class DataStatistics4TestPDF(unittest.TestCase):
    def test_pdf(self):
        self.assertEqual(DataStatistics4.pdf([1, 2, 3], 1, 1),
                         [0.3989422804014327, 0.24197072451914337, 0.05399096651318806])

    def test_pdf_2(self):
        self.assertEqual(DataStatistics4.pdf([1, 1, 1], 1, 1),
                         [0.3989422804014327, 0.3989422804014327, 0.3989422804014327])

    def test_pdf_3(self):
        self.assertEqual(DataStatistics4.pdf([1, 2, 3], 2, 1),
                         [0.24197072451914337, 0.3989422804014327, 0.24197072451914337])

    def test_pdf_4(self):
        self.assertEqual(DataStatistics4.pdf([1, 2, 3], 1, 2),
                         [0.19947114020071635, 0.17603266338214976, 0.12098536225957168])

    def test_pdf_5(self):
        self.assertEqual(DataStatistics4.pdf([1, 2, 3], 2, 2),
                         [0.17603266338214976, 0.19947114020071635, 0.17603266338214976])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
