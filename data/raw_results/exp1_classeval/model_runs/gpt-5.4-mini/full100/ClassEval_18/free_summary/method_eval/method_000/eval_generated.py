class CamelCaseMap:
    def __init__(self):
        self._data = {}

    def _to_camel_case(self, s):
        parts = s.split("_")
        if not parts:
            return s
        return parts[0] + "".join(part.title() for part in parts[1:])

    def _convert_key(self, key):
        if isinstance(key, str):
            return self._to_camel_case(key)
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
