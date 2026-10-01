import itertools

class ArrangementCalculator:
    def __init__(self, datas):
        self.datas = datas

    def count(self, n: int, m: int or None) -> int:
        if m is None or n == m:
            return self.factorial(n)
        else:
            return self.factorial(n) // self.factorial(n - m)

    def count_all(self, n: int) -> int:
        total = 0
        for i in range(1, n + 1):
            total += self.count(n, i)
        return total

    def factorial(self, n: int) -> int:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def select(self, m=None):
        if m is None:
            m = len(self.datas)
        result = []
        for perm in itertools.permutations(self.datas, m):
            result.append(list(perm))
        return result

    def select_all(self):
        result = []
        for i in range(1, len(self.datas) + 1):
            result.extend(self.select(i))
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
