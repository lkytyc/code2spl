class BinaryDataProcessor:
    def __init__(self, binary_string):
        self.binary_string = ''.join(c for c in binary_string if c in '01')

    def calculate_binary_info(self):
        length = len(self.binary_string)
        if length == 0:
            zeros = 0.0
            ones = 0.0
        else:
            zeros = self.binary_string.count('0') / length
            ones = self.binary_string.count('1') / length
        return {
            'Zeros': zeros,
            'Ones': ones,
            'Bit Length': length
        }

    def convert_to_ascii(self):
        return self._decode('ascii')

    def convert_to_utf8(self):
        return self._decode('utf-8')

    def _decode(self, encoding):
        byte_array = bytearray()
        for i in range(0, len(self.binary_string) - len(self.binary_string) % 8, 8):
            byte_array.append(int(self.binary_string[i:i+8], 2))
        return byte_array.decode(encoding)

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
