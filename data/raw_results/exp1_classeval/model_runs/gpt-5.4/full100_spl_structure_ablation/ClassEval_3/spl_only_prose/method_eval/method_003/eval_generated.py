class ArrangementCalculator:
    def __init__(self, datas):
        self.datas = datas

    @staticmethod
    def count(n, m):
        if m is None:
            return ArrangementCalculator.factorial(n)
        if n == m:
            return ArrangementCalculator.factorial(n)
        return ArrangementCalculator.factorial(n) // ArrangementCalculator.factorial(n - m)

    @staticmethod
    def count_all(n):
        total = 0
        for i in range(1, n + 1):
            total += ArrangementCalculator.count(n, i)
        return total

    @staticmethod
    def factorial(n):
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    def select(self, m=None):
        import itertools

        if m is None:
            m = len(self.datas)
        result = []
        for permutation in itertools.permutations(self.datas, m):
            result.append(list(permutation))
        return result

    def select_all(self):
        result = []
        for i in range(1, len(self.datas) + 1):
            result.extend(self.select(i))
        return result

import unittest

class ArrangementCalculatorTestSelectAll(unittest.TestCase):
    def test_select_all_1(self):
        ac = ArrangementCalculator([1, 2, 3])
        res = ac.select_all()
        expected = [[1], [2], [3], [1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2], [1, 2, 3], [1, 3, 2], [2, 1, 3],
                    [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        self.assertEqual(res, expected)

    def test_select_all_2(self):
        ac = ArrangementCalculator([1, 2, 4])
        res = ac.select_all()
        expected = [[1], [2], [4], [1, 2], [1, 4], [2, 1], [2, 4], [4, 1], [4, 2], [1, 2, 4], [1, 4, 2], [2, 1, 4],
                    [2, 4, 1], [4, 1, 2], [4, 2, 1]]
        self.assertEqual(res, expected)

    def test_select_all_3(self):
        ac = ArrangementCalculator([1, 2])
        res = ac.select_all()
        expected = [[1], [2], [1, 2], [2, 1]]
        self.assertEqual(res, expected)

    def test_select_all_4(self):
        ac = ArrangementCalculator([1, 3])
        res = ac.select_all()
        expected = [[1], [3], [1, 3], [3, 1]]
        self.assertEqual(res, expected)

    def test_select_all_5(self):
        ac = ArrangementCalculator([1])
        res = ac.select_all()
        expected = [[1]]
        self.assertEqual(res, expected)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
