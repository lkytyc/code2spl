class BitStatusUtil:
    @staticmethod
    def check(*values):
        for value in values:
            if not isinstance(value, int) or isinstance(value, bool) or value < 0 or value % 2 != 0:
                raise ValueError(f"{value} is not a non-negative even integer")

    @staticmethod
    def add(mask, flag):
        BitStatusUtil.check(mask, flag)
        return mask | flag

    @staticmethod
    def has(mask, flag):
        BitStatusUtil.check(mask, flag)
        return (mask & flag) == flag

    @staticmethod
    def remove(mask, flag):
        BitStatusUtil.check(mask, flag)
        if (mask & flag) == flag:
            return mask ^ flag
        return mask

import unittest

class BitStatusUtilTestCheck(unittest.TestCase):
    def test_check(self):
        bit_status_util = BitStatusUtil()
        bit_status_util.check([2])

    def test_check_2(self):
        bit_status_util = BitStatusUtil()
        with self.assertRaises(ValueError):
            bit_status_util.check([3])

    def test_check_3(self):
        bit_status_util = BitStatusUtil()
        with self.assertRaises(ValueError):
            bit_status_util.check([-1])

    def test_check_4(self):
        bit_status_util = BitStatusUtil()
        with self.assertRaises(ValueError):
            bit_status_util.check([2, 3, 4])

    def test_check_5(self):
        bit_status_util = BitStatusUtil()
        with self.assertRaises(ValueError):
            bit_status_util.check([2, 3, 4, 5])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
