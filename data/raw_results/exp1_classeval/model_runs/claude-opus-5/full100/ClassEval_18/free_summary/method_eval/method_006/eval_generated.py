class CamelCaseMap:
    def __init__(self):
        self._data = {}

    def _to_camel_case(self, key: str) -> str:
        parts = key.split('_')
        return parts[0] + ''.join(part.title() for part in parts[1:])

    def _convert_key(self, key):
        if isinstance(key, str):
            return self._to_camel_case(key)
        return key

    def __setitem__(self, key, value):
        self._data[self._convert_key(key)] = value

    def __getitem__(self, key):
        return self._data[self._convert_key(key)]

    def __delitem__(self, key):
        del self._data[self._convert_key(key)]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

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
