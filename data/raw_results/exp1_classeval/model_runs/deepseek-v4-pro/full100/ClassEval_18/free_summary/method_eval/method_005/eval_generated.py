class CamelCaseMap:
    def __init__(self):
        self._data = {}

    def _convert_key(self, key):
        if isinstance(key, str):
            parts = key.split('_')
            return parts[0] + ''.join(part.capitalize() for part in parts[1:])
        return key

    def __getitem__(self, key):
        return self._data[self._convert_key(key)]

    def __setitem__(self, key, value):
        self._data[self._convert_key(key)] = value

    def __delitem__(self, key):
        del self._data[self._convert_key(key)]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

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
