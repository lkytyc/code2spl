import math

class CombinationCalculator:
    def __init__(self, items):
        self.items = items

    @staticmethod
    def count(n, m):
        if m == 0 or m == n:
            return 1
        return math.factorial(n) // (math.factorial(m) * math.factorial(n - m))

    @staticmethod
    def count_all(n):
        if n < 0 or n > 63:
            return False
        if n == 63:
            return math.inf
        return (1 << n) - 1

    def select(self, m):
        result = []
        self._select(m, 0, [], result)
        return result

    def select_all(self):
        result = []
        for m in range(1, len(self.items) + 1):
            result.extend(self.select(m))
        return result

    def _select(self, m, start, current, result):
        if len(current) == m:
            result.append(list(current))
            return
        for i in range(start, len(self.items)):
            current.append(self.items[i])
            self._select(m, i + 1, current, result)
            current.pop()

import unittest

class CombinationCalculatorTestSelect(unittest.TestCase):
    def test_select(self):
        calc = CombinationCalculator(["A", "B", "C", "D"])
        self.assertEqual(calc.count(4, 2), 6)

    def test_select_2(self):
        calc = CombinationCalculator(["A", "B", "C", "D"])
        self.assertEqual(calc.count(5, 3), 10)

    def test_select_3(self):
        calc = CombinationCalculator(["A", "B", "C", "D"])
        self.assertEqual(calc.count(6, 6), 1)

    def test_select_4(self):
        calc = CombinationCalculator(["A", "B", "C", "D"])
        self.assertEqual(calc.count(6, 0), 1)

    def test_select_5(self):
        calc = CombinationCalculator(["A", "B", "C", "D"])
        self.assertEqual(calc.count(6, 3), 20)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
