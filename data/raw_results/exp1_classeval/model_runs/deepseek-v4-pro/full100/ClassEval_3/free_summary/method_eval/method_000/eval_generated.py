class ArrangementCalculator:
    def __init__(self, datas):
        self.datas = list(datas)

    @staticmethod
    def factorial(n):
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def count(self, n, m=None):
        if m is None or m == n:
            return self.factorial(n)
        if m > n or m < 0:
            return 0
        return self.factorial(n) // self.factorial(n - m)

    def count_all(self, n):
        return sum(self.count(n, m) for m in range(1, n + 1))

    def select(self, m=None):
        import itertools
        if m is None:
            m = len(self.datas)
        return list(itertools.permutations(self.datas, m))

    def select_all(self):
        result = []
        for m in range(1, len(self.datas) + 1):
            result.extend(self.select(m))
        return result

import unittest

class ArrangementCalculatorTestCount(unittest.TestCase):
    def test_count_1(self):
        res = ArrangementCalculator.count(5, 3)
        self.assertEqual(res, 60)

    def test_count_2(self):
        res = ArrangementCalculator.count(4, 3)
        self.assertEqual(res, 24)

    def test_count_3(self):
        res = ArrangementCalculator.count(6, 3)
        self.assertEqual(res, 120)

    def test_count_4(self):
        res = ArrangementCalculator.count(7, 3)
        self.assertEqual(res, 210)

    def test_count_5(self):
        res = ArrangementCalculator.count(4, 4)
        self.assertEqual(res, 24)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
