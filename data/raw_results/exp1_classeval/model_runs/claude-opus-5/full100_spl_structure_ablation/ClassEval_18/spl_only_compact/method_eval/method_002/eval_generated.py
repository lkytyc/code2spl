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
