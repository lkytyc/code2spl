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

class CamelCaseMapTestGetitem(unittest.TestCase):
    def test_getitem_1(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        self.assertEqual(camelize_map.__getitem__('first_name'), 'John')

    def test_getitem_2(self):
        camelize_map = CamelCaseMap()
        camelize_map['last_name'] = 'Doe'
        self.assertEqual(camelize_map.__getitem__('last_name'), 'Doe')

    def test_getitem_3(self):
        camelize_map = CamelCaseMap()
        camelize_map['age'] = 30
        self.assertEqual(camelize_map.__getitem__('age'), 30)

    def test_getitem_4(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        self.assertEqual(camelize_map.__getitem__('first_Name'), 'John')

    def test_getitem_5(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        self.assertEqual(camelize_map.__getitem__('firstName'), 'John')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
