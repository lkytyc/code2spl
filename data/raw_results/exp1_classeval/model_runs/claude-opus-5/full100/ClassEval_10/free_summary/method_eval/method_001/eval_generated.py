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

class BinaryDataProcessorTestCalculateBinaryInfo(unittest.TestCase):
    def test_calculate_binary_info(self):
        bdp = BinaryDataProcessor("0110100001100101011011000110110001101111")
        self.assertEqual(bdp.calculate_binary_info(), {'Zeroes': 0.475, 'Ones': 0.525, 'Bit length': 40})

    def test_calculate_binary_info_2(self):
        bdp = BinaryDataProcessor("0110100001100101011010011111")
        self.assertEqual(bdp.calculate_binary_info(), {'Bit length': 28, 'Ones': 0.5357142857142857, 'Zeroes': 0.4642857142857143})

    def test_calculate_binary_info_3(self):
        bdp = BinaryDataProcessor("01101001111100101011010011111")
        self.assertEqual(bdp.calculate_binary_info(), {'Bit length': 29, 'Ones': 0.6206896551724138, 'Zeroes': 0.3793103448275862})

    def test_calculate_binary_info_4(self):
        bdp = BinaryDataProcessor("011010011111001")
        self.assertEqual(bdp.calculate_binary_info(), {'Bit length': 15, 'Ones': 0.6, 'Zeroes': 0.4})

    def test_calculate_binary_info_5(self):
        bdp = BinaryDataProcessor("0110100111110010")
        self.assertEqual(bdp.calculate_binary_info(), {'Bit length': 16, 'Ones': 0.5625, 'Zeroes': 0.4375})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
