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

class BitStatusUtilTestRemove(unittest.TestCase):
    def test_remove(self):
        bit_status_util = BitStatusUtil()
        self.assertEqual(bit_status_util.remove(6, 2), 4)

    def test_remove_2(self):
        bit_status_util = BitStatusUtil()
        self.assertEqual(bit_status_util.remove(8, 2), 8)

    def test_remove_3(self):
        bit_status_util = BitStatusUtil()
        self.assertEqual(bit_status_util.remove(6, 4), 2)

    def test_remove_4(self):
        bit_status_util = BitStatusUtil()
        self.assertEqual(bit_status_util.remove(8, 6), 8)

    def test_remove_5(self):
        bit_status_util = BitStatusUtil()
        self.assertEqual(bit_status_util.remove(6, 6), 0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
