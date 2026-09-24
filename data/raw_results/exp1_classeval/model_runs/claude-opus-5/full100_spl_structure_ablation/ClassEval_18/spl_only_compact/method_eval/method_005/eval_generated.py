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

class CamelCaseMapTestConvertKey(unittest.TestCase):
    def test_convert_key_1(self):
        camelize_map = CamelCaseMap()
        self.assertEqual(camelize_map._convert_key('aaa_bbb'), 'aaaBbb')

    def test_convert_key_2(self):
        camelize_map = CamelCaseMap()
        self.assertEqual(camelize_map._convert_key('first_name'), 'firstName')

    def test_convert_key_3(self):
        camelize_map = CamelCaseMap()
        self.assertEqual(camelize_map._convert_key('last_name'), 'lastName')

    def test_convert_key_4(self):
        camelize_map = CamelCaseMap()
        self.assertEqual(camelize_map._convert_key('ccc_ddd'), 'cccDdd')

    def test_convert_key_5(self):
        camelize_map = CamelCaseMap()
        self.assertEqual(camelize_map._convert_key('eee_fff'), 'eeeFff')

    def test_convert_key_6(self):
        camelize_map = CamelCaseMap()
        self.assertEqual(camelize_map._convert_key(1234), 1234)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
