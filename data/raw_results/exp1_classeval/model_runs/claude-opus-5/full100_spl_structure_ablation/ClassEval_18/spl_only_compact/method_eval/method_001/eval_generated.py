class CamelCaseMap:
    def __init__(self):
        self._data = {}

    def _convert_key(self, key):
        is_string = isinstance(key, str)
        if is_string:
            camel_case_result = self._to_camel_case(key)
            return camel_case_result
        return key

    def _to_camel_case(self, key):
        parts = key.split('_')
        head = parts[0]
        tail_segments = [part.title() for part in parts[1:]]
        tail = ''.join(tail_segments)
        return_value = head + tail
        return return_value

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
