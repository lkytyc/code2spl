class BinaryDataProcessor:
    def __init__(self, binary_string):
        self.binary_string = binary_string
        self.clean_non_binary_chars()

    def clean_non_binary_chars(self):
        current_binary_string = self.binary_string
        filtered_binary_chars = [char for char in current_binary_string if char in ("0", "1")]
        clean_binary_string = "".join(filtered_binary_chars)
        self.binary_string = clean_binary_string

    def calculate_binary_info(self):
        zeroes_count = self.binary_string.count("0")
        ones_count = self.binary_string.count("1")
        total_length = len(self.binary_string)
        zeroes_percentage = zeroes_count / total_length
        ones_percentage = ones_count / total_length
        result = {
            "Zeroes": zeroes_percentage,
            "Ones": ones_percentage,
            "Bit length": total_length,
        }
        return result

    def convert_to_ascii(self):
        byte_array = bytearray()
        for i in range(0, len(self.binary_string), 8):
            binary_slice = self.binary_string[i:i + 8]
            byte_array.append(int(binary_slice, 2))
        result = byte_array.decode("ascii")
        return result

    def convert_to_utf8(self):
        byte_array = bytearray()
        for i in range(0, len(self.binary_string), 8):
            binary_slice = self.binary_string[i:i + 8]
            byte_array.append(int(binary_slice, 2))
        result = byte_array.decode("utf-8")
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
