class DataStatistics:
    @staticmethod
    def mean(data):
        total_sum = sum(data)
        data_length = len(data)
        mean_value = total_sum / data_length
        rounded_mean = round(mean_value, 2)
        return rounded_mean

    def median(self, data):
        try:
            sorted_data = sorted(data)
        except TypeError as exc:
            raise TypeError(
                "Raised when the input cannot be sorted due to invalid or "
                "non-comparable elements."
            ) from exc

        n = len(sorted_data)
        parity_check = n % 2 == 0

        if parity_check:
            middle = n // 2
            return round((sorted_data[middle - 1] + sorted_data[middle]) / 2, 2)

        middle = n // 2
        return sorted_data[middle]

    @staticmethod
    def mode(data):
        counter = {}
        for item in data:
            counter[item] = counter.get(item, 0) + 1

        mode_count = max(counter.values())
        mode = [item for item, count in counter.items() if count == mode_count]
        return mode

import unittest

class DataStatisticsTestMedian(unittest.TestCase):
    def test_median_1(self):
        ds = DataStatistics()
        res = ds.median([2, 5, 1, 3, 4])
        self.assertEqual(res, 3)

    def test_median_2(self):
        ds = DataStatistics()
        res = ds.median([2, 5, 1, 3, 4, 6])
        self.assertEqual(res, 3.50)

    def test_median_3(self):
        ds = DataStatistics()
        res = ds.median([2, 5, 1, 4, 6, 7])
        self.assertEqual(res, 4.5)

    def test_median_4(self):
        ds = DataStatistics()
        res = ds.median([2, 5, 1, 4, 6, 7, 8])
        self.assertEqual(res, 5)

    def test_median_5(self):
        ds = DataStatistics()
        res = ds.median([2, 5, 1, 4, 6, 7, 8, 9])
        self.assertEqual(res, 5.5)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
