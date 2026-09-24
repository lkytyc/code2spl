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

class BinaryDataProcessorTestCleanNonBinaryChars(unittest.TestCase):
    def test_clean_non_binary_chars(self):
        bdp = BinaryDataProcessor("01101000daf3e4r01100101011011000110110001101111")
        self.assertEqual(bdp.binary_string, "0110100001100101011011000110110001101111")

    def test_clean_non_binary_chars_2(self):
        bdp = BinaryDataProcessor("01101000daf3e4r01100101011011addf0110001d1111")
        self.assertEqual(bdp.binary_string, "011010000110010101101101100011111")

    def test_clean_non_binary_chars_3(self):
        bdp = BinaryDataProcessor("0sd1000daf3e4r01100101011011addf0110001d1111")
        self.assertEqual(bdp.binary_string, "010000110010101101101100011111")

    def test_clean_non_binary_chars_4(self):
        bdp = BinaryDataProcessor("sdsdf")
        self.assertEqual(bdp.binary_string, "")

    def test_clean_non_binary_chars_5(self):
        bdp = BinaryDataProcessor("0")
        self.assertEqual(bdp.binary_string, "0")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
