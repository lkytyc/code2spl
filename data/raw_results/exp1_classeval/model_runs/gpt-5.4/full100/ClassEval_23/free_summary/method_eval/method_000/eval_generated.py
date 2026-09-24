class CombinationCalculator:
    def __init__(self, datas):
        self.datas = datas

    def count(self, n, m):
        if m < 0 or n < 0 or m > n:
            return 0
        if m == 0 or n == m:
            return 1
        m = min(m, n - m)
        result = 1
        for i in range(1, m + 1):
            result = result * (n - m + i) // i
        return result

    def count_all(self, n):
        if n < 0 or n > 63:
            return False
        if n == 63:
            return float("inf")
        return (1 << n) - 1

    def select(self, m):
        if m < 0 or m > len(self.datas):
            return []
        result = []
        self._select(0, m, [], result)
        return result

    def select_all(self):
        result = []
        for m in range(1, len(self.datas) + 1):
            self._select(0, m, [], result)
        return result

    def _select(self, start, m, current, result):
        if len(current) == m:
            result.append(current[:])
            return
        remaining_needed = m - len(current)
        end = len(self.datas) - remaining_needed + 1
        for i in range(start, end):
            current.append(self.datas[i])
            self._select(i + 1, m, current, result)
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
