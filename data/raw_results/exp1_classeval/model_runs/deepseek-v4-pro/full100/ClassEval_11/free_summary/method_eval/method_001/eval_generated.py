class BitStatusUtil:
    @staticmethod
    def add(states, stat):
        BitStatusUtil.check([states, stat])
        return states | stat

    @staticmethod
    def has(states, stat):
        BitStatusUtil.check([states, stat])
        return (states & stat) == stat

    @staticmethod
    def remove(states, stat):
        BitStatusUtil.check([states, stat])
        if BitStatusUtil.has(states, stat):
            return states ^ stat
        return states

    @staticmethod
    def check(args):
        for arg in args:
            if arg < 0 or arg % 2 != 0:
                raise ValueError("All arguments must be non-negative even integers")

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
