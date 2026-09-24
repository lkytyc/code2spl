class CamelCaseMap:
    """
    This is a custom class that allows keys to be in camel case style by converting them from underscore style, which provides dictionary-like functionality.
    """

    def __init__(self):
        self._data = {}

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

    def _convert_key(self, key):
        if isinstance(key, str):
            return self._to_camel_case(key)
        return key

    @staticmethod
    def _to_camel_case(key):
        parts = key.split('_')
        head = parts[0]
        tail = ''.join(segment.title() for segment in parts[1:])
        return head + tail

import unittest

class CamelCaseMapTestDelitem(unittest.TestCase):
    def test_delitem_1(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map['last_name'] = 'Doe'
        camelize_map.__delitem__('first_name')
        self.assertEqual(camelize_map['last_name'], 'Doe')

    def test_delitem_2(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map.__delitem__('first_name')
        self.assertEqual('first_name' in camelize_map, False)

    def test_delitem_3(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map.__delitem__('first_Name')
        self.assertEqual('first_name' in camelize_map, False)

    def test_delitem_4(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = 'John'
        camelize_map.__delitem__('firstName')
        self.assertEqual('first_name' in camelize_map, False)

    def test_delitem_5(self):
        camelize_map = CamelCaseMap()
        camelize_map['first_name'] = ''
        camelize_map.__delitem__('first_name')
        self.assertEqual('first_name' in camelize_map, False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
