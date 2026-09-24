import numpy as np

class KappaCalculator:
    """
    This is a class as KappaCalculator, supporting to calculate Cohen's and Fleiss' kappa coefficient.
    """


    @staticmethod
    def kappa(testData, k):
        """
        Calculate the cohens kappa value of a k-dimensional matrix
        :param testData: The k-dimensional matrix that needs to calculate the cohens kappa value
        :param k: int, Matrix dimension
        :return:float, the cohens kappa value of the matrix
        >>> KappaCalculator.kappa([[2, 1, 1], [1, 2, 1], [1, 1, 2]], 3)
        0.25
        """
        data = np.array(testData)
        total = data.sum()
        p0 = np.trace(data) / total
        row_sums = data.sum(axis=1)
        col_sums = data.sum(axis=0)
        pe = (row_sums @ col_sums) / (total ** 2)
        if pe == 1:
            return 1.0
        return (p0 - pe) / (1 - pe)

    @staticmethod
    def fleiss_kappa(testData, N, k, n):
        """
        Calculate the fliss kappa value of an N * k matrix
        :param testData: Input data matrix, N * k
        :param N: int, Number of samples
        :param k: int, Number of categories
        :param n: int, Number of raters
        :return: float, fleiss kappa value
        >>> KappaCalculator.fleiss_kappa([[0, 0, 0, 0, 14],
        >>>                              [0, 2, 6, 4, 2],
        >>>                              [0, 0, 3, 5, 6],
        >>>                              [0, 3, 9, 2, 0],
        >>>                              [2, 2, 8, 1, 1],
        >>>                              [7, 7, 0, 0, 0],
        >>>                              [3, 2, 6, 3, 0],
        >>>                              [2, 5, 3, 2, 2],
        >>>                              [6, 5, 2, 1, 0],
        >>>                              [0, 2, 2, 3, 7]], 10, 5, 14)
        0.20993070442195522
        """
        data = np.array(testData)
        row_sums = data.sum(axis=1)
        p_i = (np.sum(data ** 2, axis=1) - n) / (n * (n - 1))
        P_bar = np.mean(p_i)
        col_sums = data.sum(axis=0)
        p_j = col_sums / (N * n)
        P_e = np.sum(p_j ** 2)
        if P_e == 1:
            return 1.0
        return (P_bar - P_e) / (1 - P_e)

import unittest

class KappaCalculatorTestFleissKappa(unittest.TestCase):
    def test_fleiss_kappa_1(self):
        self.assertEqual(KappaCalculator.fleiss_kappa([[0, 0, 0, 0, 14],
                                                       [0, 2, 6, 4, 2],
                                                       [0, 0, 3, 5, 6],
                                                       [0, 3, 9, 2, 0],
                                                       [2, 2, 8, 1, 1],
                                                       [7, 7, 0, 0, 0],
                                                       [3, 2, 6, 3, 0],
                                                       [2, 5, 3, 2, 2],
                                                       [6, 5, 2, 1, 0],
                                                       [0, 2, 2, 3, 7]], 10, 5, 14), 0.20993070442195522)

    def test_fleiss_kappa_2(self):
        self.assertEqual(KappaCalculator.fleiss_kappa([[1, 0, 0, 0, 14],
                                                       [0, 2, 6, 4, 2],
                                                       [0, 0, 3, 5, 6],
                                                       [0, 3, 9, 2, 0],
                                                       [2, 2, 8, 1, 1],
                                                       [7, 7, 0, 0, 0],
                                                       [3, 2, 6, 3, 0],
                                                       [2, 5, 3, 2, 2],
                                                       [6, 5, 2, 1, 0],
                                                       [0, 2, 2, 3, 7]], 10, 5, 14), 0.2115748928799344)

    def test_fleiss_kappa_3(self):
        self.assertEqual(KappaCalculator.fleiss_kappa([[0, 1, 0, 0, 14],
                                                       [0, 2, 6, 4, 2],
                                                       [0, 0, 3, 5, 6],
                                                       [0, 3, 9, 2, 0],
                                                       [2, 2, 8, 1, 1],
                                                       [7, 7, 0, 0, 0],
                                                       [3, 2, 6, 3, 0],
                                                       [2, 5, 3, 2, 2],
                                                       [6, 5, 2, 1, 0],
                                                       [0, 2, 2, 3, 7]], 10, 5, 14), 0.21076904123090398)

    def test_fleiss_kappa_4(self):
        self.assertEqual(KappaCalculator.fleiss_kappa([[0, 0, 1, 0, 14],
                                                       [0, 2, 6, 4, 2],
                                                       [0, 0, 3, 5, 6],
                                                       [0, 3, 9, 2, 0],
                                                       [2, 2, 8, 1, 1],
                                                       [7, 7, 0, 0, 0],
                                                       [3, 2, 6, 3, 0],
                                                       [2, 5, 3, 2, 2],
                                                       [6, 5, 2, 1, 0],
                                                       [0, 2, 2, 3, 7]], 10, 5, 14), 0.2096583016522883)

    def test_fleiss_kappa_5(self):
        self.assertEqual(KappaCalculator.fleiss_kappa([[0, 0, 0, 1, 14],
                                                       [0, 2, 6, 4, 2],
                                                       [0, 0, 3, 5, 6],
                                                       [0, 3, 9, 2, 0],
                                                       [2, 2, 8, 1, 1],
                                                       [7, 7, 0, 0, 0],
                                                       [3, 2, 6, 3, 0],
                                                       [2, 5, 3, 2, 2],
                                                       [6, 5, 2, 1, 0],
                                                       [0, 2, 2, 3, 7]], 10, 5, 14), 0.21147425143148907)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
