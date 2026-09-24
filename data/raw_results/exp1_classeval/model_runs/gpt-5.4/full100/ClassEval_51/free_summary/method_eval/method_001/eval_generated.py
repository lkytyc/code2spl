import numpy as np


class KappaCalculator:
    @staticmethod
    def kappa(testData, k):
        dataMat = np.mat(testData)
        P0 = 0.0
        for i in range(k):
            P0 += dataMat[i, i]
        xsum = np.sum(dataMat, axis=1)
        ysum = np.sum(dataMat, axis=0)
        total = np.sum(xsum)
        Pe = 0.0
        for i in range(k):
            Pe += xsum[i, 0] * ysum[0, i]
        P0 = float(P0) / float(total)
        Pe = float(Pe) / float(total * total)
        return (P0 - Pe) / (1 - Pe)

    @staticmethod
    def fleiss_kappa(testData, N, k, n):
        dataMat = np.mat(testData, dtype=float)
        oneMat = np.ones((k, 1))
        P0 = 0.0
        for i in range(N):
            row = dataMat[i, :]
            rowsum = np.sum(row)
            rowsquare = np.sum(np.multiply(row, row))
            Pi = (rowsquare - rowsum) / (n * (n - 1))
            P0 += Pi
        P0 = float(P0) / float(N)
        colTotals = np.sum(dataMat, axis=0)
        p = colTotals / (N * n)
        Pe = float((np.multiply(p, p) * oneMat)[0, 0])
        return (P0 - Pe) / (1 - Pe)

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
