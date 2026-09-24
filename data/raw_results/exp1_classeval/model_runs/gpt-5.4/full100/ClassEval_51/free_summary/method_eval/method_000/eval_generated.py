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

class KappaCalculatorTestKappa(unittest.TestCase):
    def test_kappa_1(self):
        self.assertEqual(KappaCalculator.kappa([[2, 1, 1], [1, 2, 1], [1, 1, 2]], 3), 0.25)

    def test_kappa_2(self):
        self.assertAlmostEqual(KappaCalculator.kappa([[2, 2, 1], [1, 2, 1], [1, 1, 2]], 3), 0.19469026548672572)

    def test_kappa_3(self):
        self.assertAlmostEqual(KappaCalculator.kappa([[2, 1, 2], [1, 2, 1], [1, 1, 2]], 3), 0.19469026548672572)

    def test_kappa_4(self):
        self.assertAlmostEqual(KappaCalculator.kappa([[2, 1, 1], [2, 2, 1], [1, 1, 2]], 3), 0.19469026548672572)

    def test_kappa_5(self):
        self.assertAlmostEqual(KappaCalculator.kappa([[2, 1, 1], [1, 2, 2], [1, 1, 2]], 3), 0.19469026548672572)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
