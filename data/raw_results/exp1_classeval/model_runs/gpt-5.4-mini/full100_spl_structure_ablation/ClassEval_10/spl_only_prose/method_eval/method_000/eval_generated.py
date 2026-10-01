class BinaryDataProcessor:
    def __init__(self, binary_string: str):
        self.binary_string = binary_string
        cleaned_binary_string = self.clean_non_binary_chars()

    def calculate_binary_info(self):
        zeroes_count = self.binary_string.count('0')
        ones_count = self.binary_string.count('1')
        total_length = len(self.binary_string)
        zeroes_percentage = zeroes_count / total_length
        ones_percentage = ones_count / total_length
        result = {
            'Zeroes': zeroes_percentage,
            'Ones': ones_percentage,
            'Bit length': total_length
        }
        return result

    def clean_non_binary_chars(self):
        current_binary_string = self.binary_string
        filtered_binary_chars = [char for char in current_binary_string if char in ('0', '1')]
        clean_binary_string = ''.join(filtered_binary_chars)
        self.binary_string = clean_binary_string

    def convert_to_ascii(self) -> str:
        byte_array = bytearray()
        for i in range(0, len(self.binary_string), 8):
            chunk = self.binary_string[i:i + 8]
            byte_array.append(int(chunk, 2))
        result = byte_array.decode('ascii')
        return result

    def convert_to_utf8(self) -> bytes:
        byte_array = bytearray()
        for i in range(0, len(self.binary_string), 8):
            chunk = self.binary_string[i:i + 8]
            byte_array.append(int(chunk, 2))
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
