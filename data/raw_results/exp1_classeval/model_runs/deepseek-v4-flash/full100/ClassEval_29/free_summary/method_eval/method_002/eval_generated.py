from collections import Counter

class DataStatistics:
    def mean(self, data):
        nums = list(data)
        if not nums:
            return 0
        return round(sum(nums) / len(nums), 2)

    def median(self, data):
        nums = sorted(data)
        n = len(nums)
        if n == 0:
            return 0
        mid = n // 2
        if n % 2 == 1:
            return round(nums[mid], 2)
        else:
            return round((nums[mid - 1] + nums[mid]) / 2, 2)

    def mode(self, data):
        nums = list(data)
        if not nums:
            return []
        counts = Counter(nums)
        max_count = max(counts.values())
        return [value for value, count in counts.items() if count == max_count]

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
