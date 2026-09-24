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
