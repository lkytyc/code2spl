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

class DataStatistics2TestGetVariance(unittest.TestCase):
    def test_get_variance_1(self):
        ds2 = DataStatistics2([1, 2, 3, 4])
        res = ds2.get_variance()
        self.assertEqual(res, 1.25)

    def test_get_variance_2(self):
        ds2 = DataStatistics2([1, 2, 203, 4])
        res = ds2.get_variance()
        self.assertEqual(res, 7551.25)

    def test_get_variance_3(self):
        ds2 = DataStatistics2([1, 4, 3, 2])
        res = ds2.get_variance()
        self.assertEqual(res, 1.25)

    def test_get_variance_4(self):
        ds2 = DataStatistics2([11, 14, 13, 12])
        res = ds2.get_variance()
        self.assertEqual(res, 1.25)

    def test_get_variance_5(self):
        ds2 = DataStatistics2([111, 114, 113, 112])
        res = ds2.get_variance()
        self.assertEqual(res, 1.25)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
