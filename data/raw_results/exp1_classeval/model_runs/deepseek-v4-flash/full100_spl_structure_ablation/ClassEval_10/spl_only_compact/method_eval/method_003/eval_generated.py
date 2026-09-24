class BinaryDataProcessor:
    def __init__(self, binary_string: str):
        self.binary_string = binary_string
        self.clean_non_binary_chars()

    def calculate_binary_info(self) -> dict:
        zeroes_count = self.binary_string.count('0')
        ones_count = self.binary_string.count('1')
        total_length = len(self.binary_string)
        if total_length == 0:
            raise ZeroDivisionError("Raised when computing a percentage with total_length equal to zero.")
        zeroes_percentage = zeroes_count / total_length
        ones_percentage = ones_count / total_length
        return {'Zeroes': zeroes_percentage, 'Ones': ones_percentage, 'Bit length': total_length}

    def clean_non_binary_chars(self):
        original_binary_string = self.binary_string
        filtered_chars = ''.join(c for c in original_binary_string if c in '01')
        sanitized_binary_string = filtered_chars
        self.binary_string = sanitized_binary_string

    def convert_to_ascii(self) -> str:
        byte_array = bytearray()
        i = 0
        while i < len(self.binary_string):
            byte = self.binary_string[i:i+8]
            decimal = int(byte, 2)
            byte_array.append(decimal)
            i += 8
        ascii_string = byte_array.decode('ascii')
        return ascii_string

    def convert_to_utf8(self) -> str:
        byte_array = bytearray()
        for i in range(0, len(self.binary_string), 8):
            byte = self.binary_string[i:i+8]
            decimal = int(byte, 2)
            byte_array.append(decimal)
        result = byte_array.decode('utf-8')
        return result

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
