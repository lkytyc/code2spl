class DataStatistics2:
    def __init__(self, data):
        import numpy as np
        self.data = np.array(data)

    def sum(self):
        import numpy as np
        return np.sum(self.data)

    def min(self):
        import numpy as np
        return np.min(self.data)

    def max(self):
        import numpy as np
        return np.max(self.data)

    def variance(self):
        import numpy as np
        return round(float(np.var(self.data)), 2)

    def std_deviation(self):
        import numpy as np
        return round(float(np.std(self.data)), 2)

    def correlation(self):
        import numpy as np
        if self.data.ndim == 1:
            return np.array([[1.0]])
        return np.corrcoef(self.data, rowvar=False)

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
