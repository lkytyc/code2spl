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

class BinaryDataProcessorTestCleanNonBinaryChars(unittest.TestCase):
    def test_clean_non_binary_chars(self):
        bdp = BinaryDataProcessor("01101000daf3e4r01100101011011000110110001101111")
        self.assertEqual(bdp.binary_string, "0110100001100101011011000110110001101111")

    def test_clean_non_binary_chars_2(self):
        bdp = BinaryDataProcessor("01101000daf3e4r01100101011011addf0110001d1111")
        self.assertEqual(bdp.binary_string, "011010000110010101101101100011111")

    def test_clean_non_binary_chars_3(self):
        bdp = BinaryDataProcessor("0sd1000daf3e4r01100101011011addf0110001d1111")
        self.assertEqual(bdp.binary_string, "010000110010101101101100011111")

    def test_clean_non_binary_chars_4(self):
        bdp = BinaryDataProcessor("sdsdf")
        self.assertEqual(bdp.binary_string, "")

    def test_clean_non_binary_chars_5(self):
        bdp = BinaryDataProcessor("0")
        self.assertEqual(bdp.binary_string, "0")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
