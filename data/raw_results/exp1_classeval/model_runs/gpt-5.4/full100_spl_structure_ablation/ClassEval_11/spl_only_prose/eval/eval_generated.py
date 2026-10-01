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


class BitStatusUtilTestMain(unittest.TestCase):
    def test_main(self):
        bit_status_util = BitStatusUtil()
        self.assertEqual(bit_status_util.add(2, 4), 6)
        self.assertTrue(bit_status_util.has(6, 2))
        self.assertEqual(bit_status_util.remove(6, 2), 4)
        with self.assertRaises(ValueError):
            bit_status_util.check([2, 3, 4])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
