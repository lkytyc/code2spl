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
