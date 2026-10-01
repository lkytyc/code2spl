import itertools

class ArrangementCalculator:
    """
    The Arrangement class provides permutation calculations and selection operations for a given set of data elements.
    """

    def __init__(self, datas):
        """
        Initializes the ArrangementCalculator object with a list of datas.
        :param datas: List, the data elements to be used for arrangements.
        """
        self.datas = datas

    @staticmethod
    def count(n, m=None):
        """
        Counts the number of arrangements by choosing m items from n items (permutations).
        If m is not provided or n equals m, returns factorial(n).
        :param n: int, the total number of items.
        :param m: int, the number of items to be chosen (default=None).
        :return: int, the count of arrangements.
        >>> ArrangementCalculator.count(5, 3)
        60
        """
        if m is None:
            return ArrangementCalculator.factorial(n)
        if n == m:
            return ArrangementCalculator.factorial(n)
        return ArrangementCalculator.factorial(n) // ArrangementCalculator.factorial(n - m)

    @staticmethod
    def count_all(n):
        """
        Counts the total number of all possible arrangements by choosing at least 1 item and at most n items from n items.
        :param n: int, the total number of items.
        :return: int, the count of all arrangements.
        >>> ArrangementCalculator.count_all(4)
        64
        """
        total = 0
        for i in range(1, n + 1):
            total += ArrangementCalculator.count(n, i)
        return total

    def select(self, m=None):
        """
        Generates a list of arrangements by selecting m items from the internal datas.
        If m is not provided, selects all items.
        :param m: int, the number of items to be chosen (default=None).
        :return: List, a list of arrangements.
        >>> ac = ArrangementCalculator([1, 2, 3, 4])
        >>> ac.select(2)
        [[1, 2], [1, 3], [1, 4], [2, 1], [2, 3], [2, 4], [3, 1], [3, 2], [3, 4], [4, 1], [4, 2], [4, 3]]
        """
        if m is None:
            m = len(self.datas)
        result = []
        for permutation in itertools.permutations(self.datas, m):
            result.append(list(permutation))
        return result

    def select_all(self):
        """
        Generates a list of all arrangements by selecting at least 1 item and at most the number of internal datas.
        :return: List, a list of all arrangements.
        >>> ac = ArrangementCalculator([1, 2, 3])
        >>> ac.select_all()
        [[1], [2], [3], [1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2], [1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        """
        result = []
        for i in range(1, len(self.datas) + 1):
            result.extend(self.select(i))
        return result

    @staticmethod
    def factorial(n):
        """
        Calculates the factorial of a given number.
        :param n: int, the number to calculate the factorial.
        :return: int, the factorial of the given number.
        >>> ArrangementCalculator.factorial(4)
        24
        """
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

import unittest

class ArrangementCalculatorTestSelectAll(unittest.TestCase):
    def test_select_all_1(self):
        ac = ArrangementCalculator([1, 2, 3])
        res = ac.select_all()
        expected = [[1], [2], [3], [1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2], [1, 2, 3], [1, 3, 2], [2, 1, 3],
                    [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        self.assertEqual(res, expected)

    def test_select_all_2(self):
        ac = ArrangementCalculator([1, 2, 4])
        res = ac.select_all()
        expected = [[1], [2], [4], [1, 2], [1, 4], [2, 1], [2, 4], [4, 1], [4, 2], [1, 2, 4], [1, 4, 2], [2, 1, 4],
                    [2, 4, 1], [4, 1, 2], [4, 2, 1]]
        self.assertEqual(res, expected)

    def test_select_all_3(self):
        ac = ArrangementCalculator([1, 2])
        res = ac.select_all()
        expected = [[1], [2], [1, 2], [2, 1]]
        self.assertEqual(res, expected)

    def test_select_all_4(self):
        ac = ArrangementCalculator([1, 3])
        res = ac.select_all()
        expected = [[1], [3], [1, 3], [3, 1]]
        self.assertEqual(res, expected)

    def test_select_all_5(self):
        ac = ArrangementCalculator([1])
        res = ac.select_all()
        expected = [[1]]
        self.assertEqual(res, expected)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
