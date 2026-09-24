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
