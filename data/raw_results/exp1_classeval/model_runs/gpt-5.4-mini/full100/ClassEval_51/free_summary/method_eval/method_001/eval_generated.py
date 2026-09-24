class KappaCalculator:
    @staticmethod
    def kappa(testData, k):
        import numpy as np

        M = np.asmatrix(testData, dtype=float)
        if M.shape != (k, k):
            M = np.asmatrix(M, dtype=float).reshape((k, k))

        n = float(np.sum(M))
        if n == 0:
            return 0.0

        po = float(np.trace(M)) / n
        row_sums = np.sum(M, axis=1)
        col_sums = np.sum(M, axis=0)
        pe = float(np.sum(np.multiply(row_sums, col_sums))) / (n * n)

        denom = 1.0 - pe
        if denom == 0:
            return 0.0
        return (po - pe) / denom

    @staticmethod
    def fleiss_kappa(testData, N, k, n):
        import numpy as np

        M = np.asmatrix(testData, dtype=float)
        if M.shape != (N, k):
            M = np.asmatrix(M, dtype=float).reshape((N, k))

        if N == 0 or n == 0:
            return 0.0

        row_sums = np.sum(M, axis=1)
        # Observed agreement per item
        Pi = []
        for i in range(N):
            counts = np.asarray(M[i, :], dtype=float).ravel()
            denom = n * (n - 1)
            if denom == 0:
                Pi.append(0.0)
            else:
                Pi.append((np.sum(counts * counts) - n) / denom)
        P_bar = float(np.mean(Pi)) if len(Pi) > 0 else 0.0

        p = np.sum(M, axis=0) / (N * n)
        P_e = float(np.sum(np.asarray(p, dtype=float) ** 2))

        denom = 1.0 - P_e
        if denom == 0:
            return 0.0
        return (P_bar - P_e) / denom

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
