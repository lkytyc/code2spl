class KappaCalculator:
    @staticmethod
    def kappa(testData, k):
        total = sum(sum(row) for row in testData)
        P0 = sum(testData[i][i] for i in range(k)) / total
        
        row_sums = [sum(row) for row in testData]
        col_sums = [sum(testData[i][j] for i in range(k)) for j in range(k)]
        Pe = sum(row_sums[i] * col_sums[i] for i in range(k)) / (total ** 2)
        
        return (P0 - Pe) / (1 - Pe)

    @staticmethod
    def fleiss_kappa(testData, N, k, n):
        P0 = 0.0
        for i in range(N):
            sum_sq = sum(testData[i][j] ** 2 for j in range(k))
            P0 += (sum_sq - n) / (n * (n - 1))
        P0 /= N
        
        col_totals = [sum(testData[i][j] for i in range(N)) for j in range(k)]
        total_assignments = N * n
        Pe = sum((col_totals[j] / total_assignments) ** 2 for j in range(k))
        
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
