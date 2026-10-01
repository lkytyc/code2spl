class BitStatusUtil:
    @staticmethod
    def add(states: int, stat: int) -> int:
        BitStatusUtil.check([states, stat])
        combined_state = states | stat
        return combined_state

    @staticmethod
    def check(args):
        for current_arg in args:
            if current_arg < 0:
                raise ValueError(f"{current_arg} must be greater than or equal to 0")
            if current_arg % 2 != 0:
                raise ValueError(f"{current_arg} not even")

    @staticmethod
    def has(states: int, stat: int) -> bool:
        BitStatusUtil.check([states, stat])
        result = (states & stat) == stat
        return result

    @staticmethod
    def remove(states: int, stat: int) -> int:
        BitStatusUtil.check([states, stat])
        if BitStatusUtil.has(states, stat):
            toggled_states = states ^ stat
            return toggled_states
        return states

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
