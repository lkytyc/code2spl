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

    @staticmethod
    def count(n, m=None):
        if m is None or m == n:
            return ArrangementCalculator.factorial(n)
        if m < 0 or m > n:
            return 0
        return ArrangementCalculator.factorial(n) // ArrangementCalculator.factorial(n - m)

    @staticmethod
    def count_all(n):
        total = 0
        for m in range(1, n + 1):
            total += ArrangementCalculator.count(n, m)
        return total

    def select(self, m=None):
        if m is None:
            m = len(self.datas)
        if m < 0 or m > len(self.datas):
            return []
        result = []
        self._permute([], self.datas, m, result)
        return result

    def _permute(self, current, remaining, m, result):
        if len(current) == m:
            result.append(current[:])
            return
        for i in range(len(remaining)):
            current.append(remaining[i])
            self._permute(current, remaining[:i] + remaining[i+1:], m, result)
            current.pop()

    def select_all(self):
        result = []
        for m in range(1, len(self.datas) + 1):
            result.extend(self.select(m))
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
