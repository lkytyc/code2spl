class BinaryDataProcessor:
    def __init__(self, binary_string):
        self.binary_string = ''.join(c for c in binary_string if c in '01')

    def calculate_binary_info(self):
        total_bits = len(self.binary_string)
        if total_bits == 0:
            return {'zeroes_percentage': 0.0, 'ones_percentage': 0.0, 'total_bits': 0}
        zeroes = self.binary_string.count('0')
        ones = self.binary_string.count('1')
        return {
            'zeroes_percentage': (zeroes / total_bits) * 100,
            'ones_percentage': (ones / total_bits) * 100,
            'total_bits': total_bits
        }

    def convert_to_ascii(self):
        if len(self.binary_string) % 8 != 0:
            raise ValueError("Binary string length must be a multiple of 8")
        byte_values = [int(self.binary_string[i:i+8], 2) for i in range(0, len(self.binary_string), 8)]
        return bytes(byte_values).decode('ascii')

    def convert_to_utf8(self):
        if len(self.binary_string) % 8 != 0:
            raise ValueError("Binary string length must be a multiple of 8")
        byte_values = [int(self.binary_string[i:i+8], 2) for i in range(0, len(self.binary_string), 8)]
        return bytes(byte_values).decode('utf-8')

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
