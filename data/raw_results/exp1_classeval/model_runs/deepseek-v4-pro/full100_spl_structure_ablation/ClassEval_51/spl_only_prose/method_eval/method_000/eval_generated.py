import numpy as np


class KappaCalculator:
    def __init__(self, testData):
        self.testData = testData

    def fleiss_kappa(self, N: int, k: int, n: int) -> float:
        dataMat = np.matrix(self.testData, dtype=float)
        oneMat = np.ones((k, 1))
        sum_val = 0.0
        P0 = 0.0
        for i in range(N):
            temp = 0.0
            for j in range(k):
                sum_val += dataMat[i, j]
                temp += 1.0 * dataMat[i, j] ** 2
            temp -= n
            temp /= (n - 1) * n
            P0 += temp
        P0 = 1.0 * P0 / N
        ysum = np.sum(dataMat, axis=0)
        for i in range(k):
            ysum[0, i] = (ysum[0, i] / sum_val) ** 2
        Pe = ysum * oneMat * 1.0
        ans = (P0 - Pe) / (1 - Pe)
        return ans[0, 0]

    def kappa(self, k: int) -> float:
        dataMat = np.matrix(self.testData)
        P0 = 0.0
        for i in range(k):
            P0 += dataMat[i, i] * 1.0
        xsum = np.sum(dataMat, axis=1)
        ysum = np.sum(dataMat, axis=0)
        sum_val = np.sum(dataMat)
        Pe = float(ysum * xsum) / sum_val / sum_val
        P0 = float(P0 / sum_val * 1.0)
        cohens_coefficient = float((P0 - Pe) / (1 - Pe))
        return cohens_coefficient

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
