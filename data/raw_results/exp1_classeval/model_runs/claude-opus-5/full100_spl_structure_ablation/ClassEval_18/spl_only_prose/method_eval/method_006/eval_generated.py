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

class CamelCaseMapTestToCamelCase(unittest.TestCase):
    def test_to_camel_case_1(self):
        self.assertEqual(CamelCaseMap._to_camel_case('aaa_bbb'), 'aaaBbb')

    def test_to_camel_case_2(self):
        self.assertEqual(CamelCaseMap._to_camel_case('first_name'), 'firstName')

    def test_to_camel_case_3(self):
        self.assertEqual(CamelCaseMap._to_camel_case('last_name'), 'lastName')

    def test_to_camel_case_4(self):
        self.assertEqual(CamelCaseMap._to_camel_case('ccc_ddd'), 'cccDdd')

    def test_to_camel_case_5(self):
        self.assertEqual(CamelCaseMap._to_camel_case('eee_fff'), 'eeeFff')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
