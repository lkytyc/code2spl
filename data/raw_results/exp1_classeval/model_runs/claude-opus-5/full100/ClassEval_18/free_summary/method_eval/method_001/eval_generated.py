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

class CamelCaseMapTestSetitem(unittest.TestCase):
    def test_setitem_1(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map.__setitem__('first_name', 'newname')
        self.assertEqual(camelize_map['first_name'], 'newname')

    def test_setitem_2(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map.__setitem__('first_name', 'John')
        self.assertEqual(camelize_map['first_name'], 'John')

    def test_setitem_3(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map.__setitem__('first_Name', 'newname')
        self.assertEqual(camelize_map['first_name'], 'newname')

    def test_setitem_4(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map.__setitem__('firstName', 'newname')
        self.assertEqual(camelize_map['first_name'], 'newname')

    def test_setitem_5(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map.__setitem__('first_name', '')
        self.assertEqual(camelize_map['first_name'], '')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
