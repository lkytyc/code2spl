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

class BitStatusUtilTestHas(unittest.TestCase):
    def test_has(self):
        bit_status_util = BitStatusUtil()
        self.assertTrue(bit_status_util.has(6, 2))

    def test_has_2(self):
        bit_status_util = BitStatusUtil()
        self.assertFalse(bit_status_util.has(8, 2))

    def test_has_3(self):
        bit_status_util = BitStatusUtil()
        self.assertTrue(bit_status_util.has(6, 4))

    def test_has_4(self):
        bit_status_util = BitStatusUtil()
        self.assertFalse(bit_status_util.has(8, 6))

    def test_has_5(self):
        bit_status_util = BitStatusUtil()
        self.assertTrue(bit_status_util.has(6, 6))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
