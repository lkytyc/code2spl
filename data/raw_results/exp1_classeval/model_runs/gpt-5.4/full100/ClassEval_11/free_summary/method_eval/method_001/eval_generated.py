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
