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
