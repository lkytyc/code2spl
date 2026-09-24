from collections import Counter


class DataStatistics:
    def mean(self, numbers):
        return round(sum(numbers) / len(numbers), 2)

    def median(self, numbers):
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        mid = n // 2
        if n % 2 == 0:
            return round((sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2, 2)
        else:
            return sorted_numbers[mid]

    def mode(self, numbers):
        counts = Counter(numbers)
        max_frequency = max(counts.values())
        return [value for value, freq in counts.items() if freq == max_frequency]

import unittest

class DataStatisticsTestMode(unittest.TestCase):
    def test_mode_1(self):
        ds = DataStatistics()
        res = ds.mode([2, 2, 3, 3, 4])
        self.assertEqual(res, [2, 3])

    def test_mode_2(self):
        ds = DataStatistics()
        res = ds.mode([2, 2, 2, 3, 3, 4])
        self.assertEqual(res, [2])

    def test_mode_3(self):
        ds = DataStatistics()
        res = ds.mode([2, 2, 3, 3, 4, 4])
        self.assertEqual(res, [2, 3, 4])

    def test_mode_4(self):
        ds = DataStatistics()
        res = ds.mode([2, 2, 3, 3, 4, 4, 4])
        self.assertEqual(res, [4])

    def test_mode_5(self):
        ds = DataStatistics()
        res = ds.mode([2, 2, 3, 3, 4, 4, 4, 5])
        self.assertEqual(res, [4])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
