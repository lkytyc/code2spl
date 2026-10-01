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
