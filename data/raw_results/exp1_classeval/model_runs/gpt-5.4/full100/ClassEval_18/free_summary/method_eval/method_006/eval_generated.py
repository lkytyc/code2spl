class CamelCaseMap:
    def __init__(self):
        self._data = {}

    def _normalize_key(self, key):
        if not isinstance(key, str):
            return key
        parts = key.split('_')
        if not parts:
            return key
        return parts[0] + ''.join(part.capitalize() for part in parts[1:])

    def __setitem__(self, key, value):
        self._data[self._normalize_key(key)] = value

    def __getitem__(self, key):
        return self._data[self._normalize_key(key)]

    def __delitem__(self, key):
        del self._data[self._normalize_key(key)]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

import unittest

class CamelCaseMapTestToCamelCase(unittest.TestCase):
    def test_to_camel_case_1(self):
        self.assertEqual(CamelCaseMap._to_camel_case('aaa_bbb'), 'aaaBbb')

    def test_to_camel_case_2(self):
        self.assertEqual(CamelCaseMap._to_camel_case('first_name'), 'firstName')

    def test_to_camel_case_3(self):
        self.assertEqual(CamelCaseMap._to_camel_case('last_name'), 'lastName')

    def test_to_camel_case_4(self):
        self.assertEqual(CamelCaseMap._to_camel_case('ccc_ddd'), 'cccDdd')

    def test_to_camel_case_5(self):
        self.assertEqual(CamelCaseMap._to_camel_case('eee_fff'), 'eeeFff')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
