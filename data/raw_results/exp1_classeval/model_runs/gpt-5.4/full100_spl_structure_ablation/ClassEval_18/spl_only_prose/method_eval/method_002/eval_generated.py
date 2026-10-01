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
