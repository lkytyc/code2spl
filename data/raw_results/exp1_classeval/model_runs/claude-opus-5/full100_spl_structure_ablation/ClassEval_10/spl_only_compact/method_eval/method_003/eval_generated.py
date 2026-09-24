class BinaryDataProcessor:
    def __init__(self, binary_string: str):
        self.binary_string = binary_string
        self.binary_string = self.clean_non_binary_chars()

    def clean_non_binary_chars(self):
        source_string = self.binary_string
        filtered_iterator = filter(lambda x: x == '0' or x == '1', source_string)
        cleaned_string = ''.join(filtered_iterator)
        self.binary_string = cleaned_string

    def calculate_binary_info(self) -> dict:
        zeroes_count = self.binary_string.count('0')
        ones_count = self.binary_string.count('1')
        total_length = len(self.binary_string)
        zeroes_percentage = zeroes_count / total_length
        ones_percentage = ones_count / total_length
        return {
            'Zeroes': zeroes_percentage,
            'Ones': ones_percentage,
            'Bit length': total_length
        }

    def convert_to_ascii(self) -> str:
        byte_array = bytearray()
        for i in range(0, len(self.binary_string), 8):
            byte = self.binary_string[i:i+8]
            if len(byte) < 8:
                break
            decimal = int(byte, 2)
            byte_array.append(decimal)
        ascii_string = byte_array.decode('ascii')
        return ascii_string

    def convert_to_utf8(self) -> str:
        byte_array = bytearray()
        for i in range(0, len(self.binary_string), 8):
            byte = self.binary_string[i:i+8]
            decimal = int(byte, 2)
            byte_array.append(decimal)
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
