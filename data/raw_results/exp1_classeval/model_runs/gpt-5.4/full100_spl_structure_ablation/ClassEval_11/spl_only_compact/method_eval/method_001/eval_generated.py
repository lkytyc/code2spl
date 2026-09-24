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
