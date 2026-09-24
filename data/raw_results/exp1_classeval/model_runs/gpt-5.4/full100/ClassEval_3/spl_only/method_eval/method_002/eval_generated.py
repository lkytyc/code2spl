import itertools


class ArrangementCalculator:
    def __init__(self, datas):
        self.datas = datas

    @staticmethod
    def count(n, m=None):
        if m is None or n == m:
            return ArrangementCalculator.factorial(n)
        return ArrangementCalculator.factorial(n) // ArrangementCalculator.factorial(n - m)

    @staticmethod
    def count_all(n):
        total = 0
        for i in range(1, n + 1):
            total += ArrangementCalculator.count(n, i)
        return total

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

    @staticmethod
    def factorial(n):
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

import unittest

class ArrangementCalculatorTestSelect(unittest.TestCase):
    def test_select_1(self):
        ac = ArrangementCalculator([1, 2, 3, 4])
        res = ac.select(2)
        expected = [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]]
        self.assertEqual(res, expected)

    def test_select_2(self):
        ac = ArrangementCalculator([1, 2, 3])
        res = ac.select(2)
        expected = [[1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2]]
        self.assertEqual(res, expected)

    def test_select_3(self):
        ac = ArrangementCalculator([2, 3, 4])
        res = ac.select(2)
        expected = [[2, 3], [2, 4], [3, 2], [3, 4], [4, 2], [4, 3]]
        self.assertEqual(res, expected)

    def test_select_4(self):
        ac = ArrangementCalculator([1, 2])
        res = ac.select(2)
        expected = [[1, 2], [2, 1]]
        self.assertEqual(res, expected)

    def test_select_5(self):
        ac = ArrangementCalculator([1, 2, 3, 4])
        res = ac.select(1)
        expected = [[1], [2], [3], [4]]
        self.assertEqual(res, expected)

    def test_select_6(self):
        ac = ArrangementCalculator([1, 2])
        res = ac.select()
        expected = [[1, 2], [2, 1]]
        self.assertEqual(res, expected)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
