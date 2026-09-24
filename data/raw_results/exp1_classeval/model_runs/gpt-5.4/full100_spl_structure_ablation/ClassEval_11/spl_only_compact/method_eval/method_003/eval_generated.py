class BitStatusUtil:
    @staticmethod
    def add(states, stat):
        BitStatusUtil.check([states, stat])
        result = states | stat
        return result

    @staticmethod
    def check(args):
        for arg in args:
            is_negative = arg < 0
            if is_negative:
                raise ValueError("arg must be greater than or equal to 0")

            is_not_even = arg % 2 != 0
            if is_not_even:
                raise ValueError("arg not even")

    @staticmethod
    def has(states: int, stat: int) -> bool:
        BitStatusUtil.check([states, stat])
        is_contained = (states & stat) == stat
        return is_contained

    @staticmethod
    def remove(states, stat):
        BitStatusUtil.check([states, stat])
        has_stat = BitStatusUtil.has(states, stat)
        if has_stat:
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
