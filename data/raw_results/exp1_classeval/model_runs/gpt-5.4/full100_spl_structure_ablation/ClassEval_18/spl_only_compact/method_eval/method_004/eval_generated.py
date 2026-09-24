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
