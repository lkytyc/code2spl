class DataStatistics:
    def mean(self, data):
        values = list(data)
        return round(sum(values) / len(values), 2)

    def median(self, data):
        values = sorted(data)
        n = len(values)
        mid = n // 2
        if n % 2 == 1:
            return values[mid]
        return round((values[mid - 1] + values[mid]) / 2, 2)

    def mode(self, data):
        from collections import Counter
        counts = Counter(data)
        if not counts:
            return []
        highest = max(counts.values())
        return [value for value, freq in counts.items() if freq == highest]

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
