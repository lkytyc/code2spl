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
