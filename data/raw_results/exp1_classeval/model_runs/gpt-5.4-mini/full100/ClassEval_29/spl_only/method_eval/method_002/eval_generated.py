class DataStatistics:
    @staticmethod
    def mean(data):
        total = sum(data)
        count = len(data)
        average = total / count
        result = round(average, 2)
        return result

    @staticmethod
    def median(data):
        sorted_data = sorted(data)
        n = len(sorted_data)
        parity_check = n % 2 == 0
        middle = n // 2
        if parity_check:
            result = round((sorted_data[middle - 1] + sorted_data[middle]) / 2, 2)
        else:
            result = sorted_data[middle]
        return result

    @staticmethod
    def mode(data):
        from collections import Counter

        counter = Counter(data)
        mode_count = max(counter.values())
        mode = [key for key, value in counter.items() if value == mode_count]
        return mode

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
