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

class CombinationCalculatorTestSelectAll(unittest.TestCase):
    def test_select_all(self):
        calc = CombinationCalculator(["A"])
        self.assertEqual(calc.select_all(), [['A']])

    def test_select_all_2(self):
        calc = CombinationCalculator(["A", "B"])
        self.assertEqual(calc.select_all(), [['A'], ['B'], ['A', 'B']])

    def test_select_all_3(self):
        calc = CombinationCalculator(["A", "B", "C"])
        self.assertEqual(calc.select_all(),[['A'], ['B'], ['C'], ['A', 'B'], ['A', 'C'], ['B', 'C'], ['A', 'B', 'C']])

    def test_select_all_4(self):
        calc = CombinationCalculator([])
        self.assertEqual(calc.select_all(),[])

    def test_select_all_5(self):
        calc = CombinationCalculator(["B"])
        self.assertEqual(calc.select_all(),[['B']])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
