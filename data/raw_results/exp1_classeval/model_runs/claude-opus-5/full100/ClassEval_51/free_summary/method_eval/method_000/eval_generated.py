import numpy as np


class InterRaterAgreement:

    @staticmethod
    def kappa(testData, k):
        """
        Compute Cohen's Kappa for two-rater agreement.

        Parameters
        ----------
        testData : array-like, shape (k, k)
            Square confusion matrix where entry [i, j] is the count of
            items rated as class i by rater 1 and class j by rater 2.
        k : int
            Number of classes.

        Returns
        -------
        float
            Cohen's kappa coefficient.
        """
        testData = np.array(testData, dtype=float)
        total = np.sum(testData)

        # Observed agreement: sum of diagonal / total
        P0 = np.sum(np.diag(testData)) / total

        # Expected agreement: outer product of marginals / total^2
        row_sums = np.sum(testData, axis=1)
        col_sums = np.sum(testData, axis=0)
        Pe = np.sum(np.outer(row_sums, col_sums)) / (total ** 2)

        return (P0 - Pe) / (1 - Pe)

    @staticmethod
    def fleiss_kappa(testData, N, k, n):
        """
        Compute Fleiss' Kappa for multi-rater agreement.

        Parameters
        ----------
        testData : array-like, shape (N, k)
            Ratings matrix where entry [i, j] is the number of raters
            who assigned subject i to category j.
        N : int
            Number of subjects.
        k : int
            Number of categories.
        n : int
            Number of raters per subject.

        Returns
        -------
        float
            Fleiss' kappa coefficient.
        """
        testData = np.array(testData, dtype=float)

        # Proportion of agreeing rater pairs for each subject
        # For subject i: (sum of n_ij*(n_ij - 1)) / (n*(n-1))
        P_subjects = np.zeros(N)
        for i in range(N):
            row = testData[i]
            P_subjects[i] = (np.sum(row * (row - 1))) / (n * (n - 1))

        # Mean observed agreement across all subjects
        P0 = np.mean(P_subjects)

        # Expected agreement: sum of squared relative category frequencies
        # p_j = (sum over subjects of n_ij) / (N * n)
        p_j = np.sum(testData, axis=0) / (N * n)
        Pe = np.sum(p_j ** 2)

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
