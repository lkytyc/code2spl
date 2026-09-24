class CombinationCalculator:
    def __init__(self, datas):
        self.datas = list(datas)

    @staticmethod
    def count(n, m):
        if m == 0 or n == m:
            return 1
        if m < 0 or n < 0 or m > n:
            return 0
        m = min(m, n - m)
        result = 1
        for i in range(1, m + 1):
            result = result * (n - m + i) // i
        return result

    @staticmethod
    def count_all(n):
        if n < 0 or n > 63:
            return False
        if n == 63:
            return float("inf")
        return (1 << n) - 1

    def _select(self, start, m, working, result):
        if len(working) == m:
            result.append(working.copy())
            return
        if start >= len(self.datas):
            return
        for i in range(start, len(self.datas)):
            working.append(self.datas[i])
            self._select(i + 1, m, working, result)
            working.pop()

    def select(self, m):
        result = []
        if m < 0 or m > len(self.datas):
            return result
        self._select(0, m, [], result)
        return result

    def select_all(self):
        result = []
        for i in range(1, len(self.datas) + 1):
            result.extend(self.select(i))
        return result

import unittest

class CombinationCalculatorTestCountAll(unittest.TestCase):
    def test_count_all(self):
        self.assertEqual(CombinationCalculator.count_all(4), 15)

    def test_count_all_2(self):
        self.assertEqual(CombinationCalculator.count_all(-1), False)

    def test_count_all_3(self):
        self.assertEqual(CombinationCalculator.count_all(65), False)

    def test_count_all_4(self):
        self.assertEqual(CombinationCalculator.count_all(0), 0)

    def test_count_all_5(self):
        self.assertEqual(CombinationCalculator.count_all(63), float("inf"))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
