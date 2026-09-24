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
