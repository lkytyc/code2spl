class DataStatistics2:
    def __init__(self, data):
        import numpy as np

        array_data = np.array(data)
        self.data = array_data

    def get_correlation(self):
        import numpy as np

        data = self.data
        correlation_matrix = np.corrcoef(data, rowvar=False)
        return correlation_matrix

    def get_max(self):
        import logging
        import numpy as np

        data = self.data
        try:
            max_value = np.max(data)
        except ValueError:
            logging.getLogger(__name__).error(
                "np.max(self.data) cannot determine a maximum for the provided data."
            )
            raise
        return max_value

    def get_min(self):
        import numpy as np

        data = self.data
        min_value = np.min(data)
        return min_value

    def get_std_deviation(self):
        import numpy as np

        std_value = np.std(self.data)
        rounded_std = round(std_value, 2)
        return rounded_std

    def get_sum(self):
        import numpy as np

        data = self.data
        sum_result = np.sum(data)
        return sum_result

    def get_variance(self):
        import numpy as np

        data = self.data
        variance = np.var(data)
        return round(variance, 2)

import unittest

class DataStatistics2TestGetSum(unittest.TestCase):
    def test_get_sum_1(self):
        ds2 = DataStatistics2([1, 2, 3, 4])
        res = ds2.get_sum()
        self.assertEqual(res, 10)

    def test_get_sum_2(self):
        ds2 = DataStatistics2([1, 2, 203, 4])
        res = ds2.get_sum()
        self.assertEqual(res, 210)

    def test_get_sum_3(self):
        ds2 = DataStatistics2([1, 2, 33, 4])
        res = ds2.get_sum()
        self.assertEqual(res, 40)

    def test_get_sum_4(self):
        ds2 = DataStatistics2([1, 2, 333, 4])
        res = ds2.get_sum()
        self.assertEqual(res, 340)

    def test_get_sum_5(self):
        ds2 = DataStatistics2([1, 2, 6, 4])
        res = ds2.get_sum()
        self.assertEqual(res, 13)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
