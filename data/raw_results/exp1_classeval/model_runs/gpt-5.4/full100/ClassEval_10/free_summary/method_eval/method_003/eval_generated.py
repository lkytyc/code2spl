class BinaryStringProcessor:
    def __init__(self, binary_string):
        self.binary_string = binary_string
        self.clean_non_binary_chars()

    def clean_non_binary_chars(self):
        self.binary_string = ''.join(ch for ch in self.binary_string if ch in ('0', '1'))

    def calculate_binary_info(self):
        total_length = len(self.binary_string)
        if total_length == 0:
            return {
                'zero_fraction': 0,
                'one_fraction': 0,
                'bit_length': 0
            }

        zero_count = self.binary_string.count('0')
        one_count = self.binary_string.count('1')

        return {
            'zero_fraction': zero_count / total_length,
            'one_fraction': one_count / total_length,
            'bit_length': total_length
        }

    def convert_to_ascii(self):
        byte_values = [
            int(self.binary_string[i:i + 8], 2)
            for i in range(0, len(self.binary_string), 8)
        ]
        return bytes(byte_values).decode('ascii')

    def convert_to_utf8(self):
        byte_values = [
            int(self.binary_string[i:i + 8], 2)
            for i in range(0, len(self.binary_string), 8)
        ]
        return bytes(byte_values).decode('utf-8')

import unittest

class BinaryDataProcessorTestConvertToUtf8(unittest.TestCase):
    def test_convert_to_utf8(self):
        bdp = BinaryDataProcessor("0110100001100101011011000110110001101111")
        self.assertEqual(bdp.convert_to_utf8(), "hello")

    def test_convert_to_utf8_2(self):
        bdp = BinaryDataProcessor("0110100001100101011011000110110001101001")
        self.assertEqual(bdp.convert_to_utf8(), "helli")

    def test_convert_to_utf8_3(self):
        bdp = BinaryDataProcessor("0110000001100101011011000110110001101111")
        self.assertEqual(bdp.convert_to_utf8(), "`ello")

    def test_convert_to_utf8_4(self):
        bdp = BinaryDataProcessor("0110101101100101011011000110110001101111")
        self.assertEqual(bdp.convert_to_utf8(), "kello")

    def test_convert_to_utf8_5(self):
        bdp = BinaryDataProcessor("0110101101100100011011000110110001101111")
        self.assertEqual(bdp.convert_to_utf8(), "kdllo")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
