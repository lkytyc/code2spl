class CamelCaseMap:
    def __init__(self: object):
        self._data = {}

    @staticmethod
    def _convert_key(key):
        if isinstance(key, str):
            return CamelCaseMap._to_camel_case(key)
        return key

    @staticmethod
    def _to_camel_case(key: str) -> str:
        parts = key.split("_")
        suffix = "".join(segment.title() for segment in parts[1:])
        return parts[0] + suffix

import unittest

class CamelCaseMapTestConvertKey(unittest.TestCase):
    def test_convert_key_1(self):
        camelize_map = CamelCaseMap()
        self.assertEqual(camelize_map._convert_key('aaa_bbb'), 'aaaBbb')

    def test_convert_key_2(self):
        camelize_map = CamelCaseMap()
        self.assertEqual(camelize_map._convert_key('first_name'), 'firstName')

    def test_convert_key_3(self):
        camelize_map = CamelCaseMap()
        self.assertEqual(camelize_map._convert_key('last_name'), 'lastName')

    def test_convert_key_4(self):
        camelize_map = CamelCaseMap()
        self.assertEqual(camelize_map._convert_key('ccc_ddd'), 'cccDdd')

    def test_convert_key_5(self):
        camelize_map = CamelCaseMap()
        self.assertEqual(camelize_map._convert_key('eee_fff'), 'eeeFff')

    def test_convert_key_6(self):
        camelize_map = CamelCaseMap()
        self.assertEqual(camelize_map._convert_key(1234), 1234)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
