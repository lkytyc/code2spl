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
