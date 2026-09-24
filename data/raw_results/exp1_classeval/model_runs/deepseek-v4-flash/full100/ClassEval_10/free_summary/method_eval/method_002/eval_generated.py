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
