import itertools

class ArrangementCalculator:
    def __init__(self, datas):
        self.datas = datas

    @staticmethod
    def count(n, m=None):
        if m is None:
            m = n
        if m < 0 or m > n:
            return 0
        return ArrangementCalculator.factorial(n) // ArrangementCalculator.factorial(n - m)

    @staticmethod
    def count_all(n):
        if n < 0:
            return 0
        total = 0
        for k in range(1, n + 1):
            total += ArrangementCalculator.count(n, k)
        return total

    def select(self, m=None):
        if m is None:
            m = len(self.datas)
        return [list(p) for p in itertools.permutations(self.datas, m)]

    def select_all(self):
        result = []
        for k in range(1, len(self.datas) + 1):
            result.extend(self.select(k))
        return result

    @staticmethod
    def factorial(n):
        if n < 0:
            return 0
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

import unittest

class ArrangementCalculatorTestFactorial(unittest.TestCase):
    def test_factorial_1(self):
        res = ArrangementCalculator.factorial(4)
        self.assertEqual(res, 24)

    def test_factorial_2(self):
        res = ArrangementCalculator.factorial(5)
        self.assertEqual(res, 120)

    def test_factorial_3(self):
        res = ArrangementCalculator.factorial(3)
        self.assertEqual(res, 6)

    def test_factorial_4(self):
        res = ArrangementCalculator.factorial(2)
        self.assertEqual(res, 2)

    def test_factorial_5(self):
        res = ArrangementCalculator.factorial(1)
        self.assertEqual(res, 1)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
