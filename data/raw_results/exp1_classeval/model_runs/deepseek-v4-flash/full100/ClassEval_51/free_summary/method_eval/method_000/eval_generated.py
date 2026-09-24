import numpy as np

class KappaCalculator:
    @staticmethod
    def kappa(testData, k):
        matrix = np.asarray(testData, dtype=float)
        total = matrix.sum()
        observed_agreement = np.trace(matrix) / total
        row_totals = matrix.sum(axis=1)
        col_totals = matrix.sum(axis=0)
        expected_agreement = np.sum(row_totals * col_totals) / (total * total)
        return float((observed_agreement - expected_agreement) / (1 - expected_agreement))

    @staticmethod
    def fleiss_kappa(testData, N, k, n):
        data = np.asarray(testData, dtype=float)
        P_i = (np.sum(data ** 2, axis=1) - n) / (n * (n - 1))
        P_bar = np.mean(P_i)
        P_j = data.sum(axis=0) / (N * n)
        P_e = np.sum(P_j ** 2)
        return float((P_bar - P_e) / (1 - P_e))

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
