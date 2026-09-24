import math


class CombinationCalculator:
    def __init__(self, datas):
        self.datas = datas

    def _select(self, dataIndex, resultList, resultIndex, result):
        resultLen = len(resultList)
        resultCount = resultIndex + 1
        if resultCount > resultLen:
            result.append(resultList.copy())
            return result

        for i in range(dataIndex, len(self.datas) + resultCount - resultLen):
            resultList[resultIndex] = self.datas[i]
            self._select(i + 1, resultList, resultIndex + 1, result)
        return result

    def count(self, n, m):
        condition_result = (m == 0 or n == m)
        if condition_result:
            return 1
        return math.factorial(n) // (math.factorial(n - m) * math.factorial(m))

    def count_all(self, n):
        range_check = (n < 0 or n > 63)
        if range_check:
            return False
        mask_value = (1 << n) - 1
        if n == 63:
            return float("inf")
        return mask_value

    def select(self, m):
        result = []
        self._select(0, [None] * m, 0, result)
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
