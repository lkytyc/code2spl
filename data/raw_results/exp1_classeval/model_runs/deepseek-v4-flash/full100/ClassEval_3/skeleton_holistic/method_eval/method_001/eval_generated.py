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

class ArrangementCalculatorTestCountAll(unittest.TestCase):
    def test_count_all_1(self):
        res = ArrangementCalculator.count_all(4)
        self.assertEqual(res, 64)

    def test_count_all_2(self):
        res = ArrangementCalculator.count_all(1)
        self.assertEqual(res, 1)

    def test_count_all_3(self):
        res = ArrangementCalculator.count_all(2)
        self.assertEqual(res, 4)

    def test_count_all_4(self):
        res = ArrangementCalculator.count_all(3)
        self.assertEqual(res, 15)

    def test_count_all_5(self):
        res = ArrangementCalculator.count_all(5)
        self.assertEqual(res, 325)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
