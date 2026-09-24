class BinaryDataProcessor:
    def __init__(self, binary_string):
        self.binary_string = binary_string
        self.clean_non_binary_chars()

    def clean_non_binary_chars(self):
        self.binary_string = ''.join(ch for ch in self.binary_string if ch in '01')
        return self.binary_string

    def calculate_binary_info(self):
        cleaned = self.binary_string
        total_length = len(cleaned)
        zero_count = cleaned.count('0')
        one_count = cleaned.count('1')
        if total_length == 0:
            zero_prop = 0
            one_prop = 0
        else:
            zero_prop = zero_count / total_length
            one_prop = one_count / total_length
        return {
            'proportion_of_zeroes': zero_prop,
            'proportion_of_ones': one_prop,
            'total_bit_length': total_length,
        }

    def _convert_to_text(self, encoding):
        byte_values = bytearray()
        cleaned = self.binary_string
        for i in range(0, len(cleaned) - len(cleaned) % 8, 8):
            chunk = cleaned[i:i + 8]
            byte_values.append(int(chunk, 2))
        return byte_values.decode(encoding)

    def convert_to_ascii(self):
        return self._convert_to_text('ascii')

    def convert_to_utf8(self):
        return self._convert_to_text('utf-8')

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
