import re

class BinaryDataProcessor:
    def __init__(self, binary_string):
        self.binary_string = re.sub(r'[^01]', '', binary_string)

    def calculate_binary_info(self):
        total = len(self.binary_string)
        ones = self.binary_string.count('1')
        zeros = self.binary_string.count('0')
        ones_percentage = ones / total
        zeros_percentage = zeros / total
        return {
            'Zeroes': zeros_percentage,
            'Ones': ones_percentage,
            'Bit length': total
        }

    def convert_to_ascii(self):
        byte_array = bytearray()
        for i in range(0, len(self.binary_string), 8):
            chunk = self.binary_string[i:i+8]
            if len(chunk) == 8:
                byte_array.append(int(chunk, 2))
        return byte_array.decode('ascii')

    def convert_to_utf8(self):
        byte_array = bytearray()
        for i in range(0, len(self.binary_string), 8):
            chunk = self.binary_string[i:i+8]
            if len(chunk) == 8:
                byte_array.append(int(chunk, 2))
        return byte_array.decode('utf-8')

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
