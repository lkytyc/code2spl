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
