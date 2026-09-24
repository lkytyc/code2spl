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
