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
