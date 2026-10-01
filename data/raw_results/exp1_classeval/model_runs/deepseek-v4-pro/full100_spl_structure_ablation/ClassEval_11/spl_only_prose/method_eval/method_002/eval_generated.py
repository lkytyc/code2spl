class BitStatusUtil:
    @staticmethod
    def add(states: int, stat: int) -> int:
        BitStatusUtil.check([states, stat])
        return states | stat

    @staticmethod
    def check(args: list[int]):
        for arg in args:
            if arg < 0:
                raise ValueError(f"{arg} must be greater than or equal to 0")
            if arg % 2 != 0:
                raise ValueError(f"{arg} not even")

    @staticmethod
    def has(states: int, stat: int) -> bool:
        BitStatusUtil.check([states, stat])
        and_result = states & stat
        return and_result == stat

    @staticmethod
    def remove(states: int, stat: int) -> int:
        BitStatusUtil.check([states, stat])
        has_flag = BitStatusUtil.has(states, stat)
        if not has_flag:
            return states
        return states ^ stat

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
