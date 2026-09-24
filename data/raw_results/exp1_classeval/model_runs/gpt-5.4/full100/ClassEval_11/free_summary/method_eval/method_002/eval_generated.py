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
