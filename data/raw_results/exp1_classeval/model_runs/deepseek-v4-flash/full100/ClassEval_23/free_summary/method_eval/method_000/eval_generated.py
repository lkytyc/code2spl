import math

class CombinationCalculator:
    def __init__(self, items):
        self.items = list(items)

    @staticmethod
    def count(n, m):
        if n < 0 or m < 0 or m > n:
            return 0
        return math.factorial(n) // (math.factorial(m) * math.factorial(n - m))

    @staticmethod
    def count_all(n):
        if not isinstance(n, int) or n < 0 or n > 63:
            return False
        if n == 63:
            return float('inf')
        return (1 << n) - 1

    def select(self, m):
        if m < 0 or m > len(self.items):
            return []
        result = []
        self._backtrack(0, m, [], result)
        return result

    def select_all(self):
        result = []
        for m in range(1, len(self.items) + 1):
            result.extend(self.select(m))
        return result

    def _backtrack(self, start, m, current, result):
        if len(current) == m:
            result.append(current[:])
            return

        for i in range(start, len(self.items)):
            current.append(self.items[i])
            self._backtrack(i + 1, m, current, result)
            current.pop()

import unittest

class CombinationCalculatorTestCount(unittest.TestCase):
    def test_count(self):
        self.assertEqual(CombinationCalculator.count(4, 2), 6)
    def test_count_2(self):
        self.assertEqual(CombinationCalculator.count(5, 3), 10)

    def test_count_3(self):
        self.assertEqual(CombinationCalculator.count(6, 6), 1)

    def test_count_4(self):
        self.assertEqual(CombinationCalculator.count(6, 0), 1)

    def test_count_5(self):
        self.assertEqual(CombinationCalculator.count(6, 3), 20)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
