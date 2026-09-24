import math

class DataStatistics4:
    """
    This is a class that performs advanced mathematical calculations and statistics, including correlation coefficient, skewness, kurtosis, and probability density function (PDF) for a normal distribution.
    """

    @staticmethod
    def correlation_coefficient(data1, data2):
        """
        Calculate the correlation coefficient of two sets of data.
        :param data1: The first set of data,list.
        :param data2: The second set of data,list.
        :return: The correlation coefficient, float.
        >>> DataStatistics4.correlation_coefficient([1, 2, 3], [4, 5, 6])
        0.9999999999999998

        """
        if len(data1) != len(data2) or len(data1) == 0:
            raise ValueError("data1 and data2 must have the same non-zero length")

        mean1 = sum(data1) / len(data1)
        mean2 = sum(data2) / len(data2)

        num = sum((x - mean1) * (y - mean2) for x, y in zip(data1, data2))
        den1 = sum((x - mean1) ** 2 for x in data1)
        den2 = sum((y - mean2) ** 2 for y in data2)

        if den1 == 0 or den2 == 0:
            raise ValueError("correlation coefficient is undefined for constant data")

        return num / math.sqrt(den1 * den2)

    @staticmethod
    def skewness(data):
        """
        Calculate the skewness of a set of data.
        :param data: The input data list, list.
        :return: The skewness, float.
        >>> DataStatistics4.skewness([1, 2, 5])
        2.3760224064818463

        """
        n = len(data)
        if n < 3:
            raise ValueError("data must contain at least 3 values")

        mean = sum(data) / n
        m2 = sum((x - mean) ** 2 for x in data) / n
        m3 = sum((x - mean) ** 3 for x in data) / n

        if m2 == 0:
            raise ValueError("skewness is undefined for constant data")

        g1 = m3 / (m2 ** 1.5)
        return math.sqrt(n * (n - 1)) / (n - 2) * g1

    @staticmethod
    def kurtosis(data):
        """
        Calculate the kurtosis of a set of data.
        :param data: The input data list, list.
        :return: The kurtosis, float.
        >>> DataStatistics4.kurtosis([1, 20,100])
        -1.5000000000000007

        """
        n = len(data)
        if n < 4:
            raise ValueError("data must contain at least 4 values")

        mean = sum(data) / n
        m2 = sum((x - mean) ** 2 for x in data) / n
        m4 = sum((x - mean) ** 4 for x in data) / n

        if m2 == 0:
            raise ValueError("kurtosis is undefined for constant data")

        g2 = m4 / (m2 ** 2) - 3
        return ((n - 1) * ((n + 1) * g2 + 6)) / ((n - 2) * (n - 3))

    @staticmethod
    def pdf(data, mu, sigma):
        """
        Calculate the probability density function (PDF) of a set of data under a normal distribution.
        :param data: The input data list, list.
        :param mu: The mean of the normal distribution, float.
        :param sigma: The standard deviation of the normal distribution, float.
        :return: The probability density function (PDF), list.
        >>> DataStatistics4.pdf([1, 2, 3], 1, 1)
        [0.3989422804014327, 0.24197072451914337, 0.05399096651318806]

        """
        if sigma <= 0:
            raise ValueError("sigma must be positive")

        coeff = 1.0 / (sigma * math.sqrt(2 * math.pi))
        return [coeff * math.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) for x in data]

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
