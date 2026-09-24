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
