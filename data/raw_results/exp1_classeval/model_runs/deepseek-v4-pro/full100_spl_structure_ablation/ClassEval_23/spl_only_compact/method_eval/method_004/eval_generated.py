import math
from typing import List

class CombinationCalculator:
    def __init__(self, datas: List[str]):
        self.datas = datas

    def _select(self, dataIndex: int, resultList: List[str], resultIndex: int, result: List[List[str]]):
        resultLen = len(resultList)
        resultCount = resultIndex + 1
        if resultCount > resultLen:
            result.append(resultList.copy())
            return
        for i in range(dataIndex, len(self.datas) + resultCount - resultLen):
            resultList[resultIndex] = self.datas[i]
            self._select(i + 1, resultList, resultIndex + 1, result)

    def count(self, n: int, m: int) -> int:
        if m == 0 or n == m:
            return 1
        n_minus_m = n - m
        fact_n = math.factorial(n)
        fact_n_minus_m = math.factorial(n_minus_m)
        fact_m = math.factorial(m)
        denominator = fact_n_minus_m * fact_m
        result = fact_n // denominator
        return result

    def count_all(self, n: int):
        invalid_range_check = n < 0 or n > 63
        if invalid_range_check:
            return False
        special_case_check = n == 63
        if special_case_check:
            return float("inf")
        return_value = (1 << n) - 1
        return return_value

    def select(self, m: int) -> List[List[str]]:
        result = []
        candidate_buffer = [None] * m
        self._select(0, candidate_buffer, 0, result)
        return result

    def select_all(self) -> List[List[str]]:
        result = []
        for i in range(1, len(self.datas) + 1):
            select_result_i = self.select(i)
            result.extend(select_result_i)
        return result

import unittest

class CombinationCalculatorTestSelect2(unittest.TestCase):
    def test_select2(self):
        calc = CombinationCalculator(["A", "B", "C", "D"])
        result = []
        calc._select(0, [None] * 2, 0, result)
        self.assertEqual(result, [['A', 'B'], ['A', 'C'], ['A', 'D'], ['B', 'C'], ['B', 'D'], ['C', 'D']])

    def test_select2_2(self):
        calc = CombinationCalculator(["A", "B", "C", "D"])
        result = []
        calc._select(0, [None] * 3, 0, result)
        self.assertEqual(result, [['A', 'B', 'C'], ['A', 'B', 'D'], ['A', 'C', 'D'], ['B', 'C', 'D']])

    def test_select2_3(self):
        calc = CombinationCalculator(["A", "B", "C", "D"])
        result = []
        calc._select(0, [None] * 1, 0, result)
        self.assertEqual(result, [['A'], ['B'], ['C'], ['D']])

    def test_select2_4(self):
        calc = CombinationCalculator(["A", "B", "C", "D"])
        result = []
        calc._select(0, [None] * 0, 0, result)
        self.assertEqual(result, [[]])

    def test_select2_5(self):
        calc = CombinationCalculator(["A", "B", "C", "D"])
        result = []
        calc._select(0, [None] * 4, 0, result)
        self.assertEqual(result, [['A', 'B', 'C', 'D']])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
