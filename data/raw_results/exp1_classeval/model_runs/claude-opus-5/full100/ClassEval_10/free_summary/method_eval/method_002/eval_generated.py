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

class BinaryDataProcessorTestConvertToAscii(unittest.TestCase):
    def test_convert_to_ascii(self):
        bdp = BinaryDataProcessor("0110100001100101011011000110110001101111")
        self.assertEqual(bdp.convert_to_ascii(), "hello")

    def test_convert_to_ascii_2(self):
        bdp = BinaryDataProcessor("0110100000100101011011000110110001101111")
        self.assertEqual(bdp.convert_to_ascii(), "h%llo")

    def test_convert_to_ascii_3(self):
        bdp = BinaryDataProcessor("01101000011011010110001001101111")
        self.assertEqual(bdp.convert_to_ascii(), "hmbo")

    def test_convert_to_ascii_4(self):
        bdp = BinaryDataProcessor("01101000011001010110001001101111")
        self.assertEqual(bdp.convert_to_ascii(), "hebo")

    def test_convert_to_ascii_5(self):
        bdp = BinaryDataProcessor("0110100001100101011011000110110001101111")
        self.assertEqual(bdp.convert_to_ascii(), "hello")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
