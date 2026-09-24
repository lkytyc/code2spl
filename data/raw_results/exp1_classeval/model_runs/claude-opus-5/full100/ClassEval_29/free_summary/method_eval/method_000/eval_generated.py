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

class DataStatisticsTestMean(unittest.TestCase):
    def test_mean_1(self):
        ds = DataStatistics()
        res = ds.mean([1, 2, 3, 4, 5])
        self.assertEqual(res, 3.00)

    def test_mean_2(self):
        ds = DataStatistics()
        res = ds.mean([1, 2, 3, 4, 5, 6])
        self.assertEqual(res, 3.50)

    def test_mean_3(self):
        ds = DataStatistics()
        res = ds.mean([1, 2, 4, 5, 6, 7])
        self.assertEqual(res, 4.17)

    def test_mean_4(self):
        ds = DataStatistics()
        res = ds.mean([1, 2, 4, 5, 6, 7, 8])
        self.assertEqual(res, 4.71)

    def test_mean_5(self):
        ds = DataStatistics()
        res = ds.mean([1, 2, 4, 5, 6, 7, 8, 9])
        self.assertEqual(res, 5.25)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
