class BitFlags:
    @staticmethod
    def add(states, stat):
        BitFlags.check((states, stat))
        return states | stat

    @staticmethod
    def has(states, stat):
        BitFlags.check((states, stat))
        return (states & stat) == stat

    @staticmethod
    def remove(states, stat):
        BitFlags.check((states, stat))
        if BitFlags.has(states, stat):
            return states ^ stat
        return states

    @staticmethod
    def check(args):
        for value in args:
            if value < 0:
                raise ValueError("Value must be non-negative")
            if value % 2 != 0:
                raise ValueError("Value must be even")

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
