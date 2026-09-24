import math

class CombinationCalculator:
    def __init__(self, datas):
        self.datas = datas

    def count(self, n, m):
        if m == 0 or n == m:
            return 1
        n_minus_m = n - m
        fact_n = math.factorial(n)
        fact_n_minus_m = math.factorial(n_minus_m)
        fact_m = math.factorial(m)
        denominator = fact_n_minus_m * fact_m
        result = fact_n // denominator
        return result

    def count_all(self, n):
        if n < 0 or n > 63:
            return False
        if n == 63:
            return float("inf")
        return (1 << n) - 1

    def select(self, m):
        result = []
        candidate_buffer = [None] * m
        self._select(0, candidate_buffer, 0, result)
        return result

    def select_all(self):
        result = []
        for i in range(1, len(self.datas) + 1):
            select_result_i = self.select(i)
            result.extend(select_result_i)
        return result

    def _select(self, dataIndex, resultList, resultIndex, result):
        resultLen = len(resultList)
        resultCount = resultIndex + 1
        if resultCount > resultLen:
            result.append(resultList.copy())
            return
        for i in range(dataIndex, len(self.datas) + resultCount - resultLen):
            resultList[resultIndex] = self.datas[i]
            self._select(i + 1, resultList, resultIndex + 1, result)

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
