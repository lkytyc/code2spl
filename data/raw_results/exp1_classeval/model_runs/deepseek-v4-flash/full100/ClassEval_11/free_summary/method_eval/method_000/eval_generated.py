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

class BitStatusUtilTestAdd(unittest.TestCase):
    def test_add(self):
        bit_status_util = BitStatusUtil()
        self.assertEqual(bit_status_util.add(2, 4), 6)

    def test_add_2(self):
        bit_status_util = BitStatusUtil()
        self.assertEqual(bit_status_util.add(2, 0), 2)

    def test_add_3(self):
        bit_status_util = BitStatusUtil()
        self.assertEqual(bit_status_util.add(0, 0), 0)

    def test_add_4(self):
        bit_status_util = BitStatusUtil()
        self.assertEqual(bit_status_util.add(0, 2), 2)

    def test_add_5(self):
        bit_status_util = BitStatusUtil()
        self.assertEqual(bit_status_util.add(2, 2), 2)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
