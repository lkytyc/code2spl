class CombinationCalculator:
    def __init__(self, datas):
        self.datas = list(datas)

    @staticmethod
    def count(n, m):
        if m < 0 or m > n:
            return 0
        if m == 0 or m == n:
            return 1
        if m > n - m:
            m = n - m
        result = 1
        for i in range(1, m + 1):
            result = result * (n - m + i) // i
        return result

    @staticmethod
    def count_all(n):
        if n < 0 or n > 63:
            return False
        if n == 63:
            return float('inf')
        return (1 << n) - 1

    def select(self, m):
        result = []
        self._select(0, [], m, result)
        return result

    def select_all(self):
        all_combinations = []
        for m in range(1, len(self.datas) + 1):
            all_combinations.extend(self.select(m))
        return all_combinations

    def _select(self, start, current, m, result):
        if len(current) == m:
            result.append(list(current))
            return
        for i in range(start, len(self.datas)):
            current.append(self.datas[i])
            self._select(i + 1, current, m, result)
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
