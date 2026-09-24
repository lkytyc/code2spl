class BitStatusUtil:

    @staticmethod
    def check(*args):
        for value in args:
            if value < 0:
                raise ValueError(f"Value must be non-negative, got {value}")
            if value % 2 != 0:
                raise ValueError(f"Value must be even (power of two or zero), got {value}")

    @staticmethod
    def add(states: int, stat: int) -> int:
        BitStatusUtil.check(states, stat)
        return states | stat

    @staticmethod
    def has(states: int, stat: int) -> bool:
        BitStatusUtil.check(states, stat)
        return (states & stat) == stat

    @staticmethod
    def remove(states: int, stat: int) -> int:
        BitStatusUtil.check(states, stat)
        if BitStatusUtil.has(states, stat):
            return states ^ stat
        return states

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
