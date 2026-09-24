class DataStatistics4:
    @staticmethod
    def correlation_coefficient(data1, data2):
        if len(data1) != len(data2) or len(data1) == 0:
            return 0
        n = len(data1)
        mean1 = sum(data1) / n
        mean2 = sum(data2) / n
        numerator = sum((x - mean1) * (y - mean2) for x, y in zip(data1, data2))
        denom1 = sum((x - mean1) ** 2 for x in data1)
        denom2 = sum((y - mean2) ** 2 for y in data2)
        denominator = (denom1 * denom2) ** 0.5
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
        std = variance ** 0.5
        if std == 0:
            return 0
        m3 = sum((x - mean) ** 3 for x in data) / n
        return m3 / (std ** 3)

    @staticmethod
    def kurtosis(data):
        n = len(data)
        if n == 0:
            return float('nan')
        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / n
        std = variance ** 0.5
        if std == 0:
            return float('nan')
        m4 = sum((x - mean) ** 4 for x in data) / n
        return m4 / (std ** 4) - 3

    @staticmethod
    def pdf(data, mu, sigma):
        import math
        if sigma == 0:
            return [float('inf') if x == mu else 0.0 for x in data]
        result = []
        for x in data:
            exponent = -((x - mu) ** 2) / (2 * sigma ** 2)
            result.append((1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(exponent))
        return result

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
