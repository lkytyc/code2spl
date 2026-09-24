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

class CamelCaseMapTestLen(unittest.TestCase):
    def test_len_1(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        self.assertEqual(camelize_map.__len__(), 1)

    def test_len_2(self):
        camelize_map = CamelCaseMap()
        camelize_map['last_name'] = 'Doe'
        self.assertEqual(camelize_map.__len__(), 1)

    def test_len_3(self):
        camelize_map = CamelCaseMap()
        camelize_map['age'] = 30
        self.assertEqual(camelize_map.__len__(), 1)

    def test_len_4(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map['last_Name'] = 'Doe'
        camelize_map['age'] = 30
        self.assertEqual(camelize_map.__len__(), 3)

    def test_len_5(self):
        camelize_map = CamelCaseMap()
        self.assertEqual(camelize_map.__len__(), 0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
