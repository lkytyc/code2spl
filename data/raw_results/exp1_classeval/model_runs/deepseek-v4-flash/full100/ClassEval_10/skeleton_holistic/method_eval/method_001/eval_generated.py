class BinaryDataProcessor:
    """
    This is a class used to process binary data, which includes functions such as clearing non 0 or 1 characters, counting binary string information, and converting to corresponding strings based on different encoding methods.
    """

    def __init__(self, binary_string):
        """
        Initialize the class with a binary string and clean it by removing all non 0 or 1 characters.
        """
        self.binary_string = binary_string
        self.clean_non_binary_chars()

    def clean_non_binary_chars(self):
        """
        Clean the binary string by removing all non 0 or 1 characters.
        """
        self.binary_string = ''.join(c for c in self.binary_string if c in '01')

    def calculate_binary_info(self):
        """
        Calculate the binary string information, including the percentage of 0 and 1, and the total length of the binary string.
        """
        total = len(self.binary_string)
        if total == 0:
            zeroes = 0.0
            ones = 0.0
        else:
            zeroes = round(self.binary_string.count('0') / total, 3)
            ones = round(self.binary_string.count('1') / total, 3)

        return {'Zeroes': zeroes, 'Ones': ones, 'Bit length': total}

    def convert_to_ascii(self):
        """
        Convert the binary string to ascii string.
        """
        byte_values = []
        for i in range(0, len(self.binary_string), 8):
            byte = self.binary_string[i:i + 8]
            if len(byte) == 8:
                byte_values.append(int(byte, 2))

        return bytes(byte_values).decode('ascii')

    def convert_to_utf8(self):
        """
        Convert the binary string to utf-8 string.
        """
        byte_values = []
        for i in range(0, len(self.binary_string), 8):
            byte = self.binary_string[i:i + 8]
            if len(byte) == 8:
                byte_values.append(int(byte, 2))

        return bytes(byte_values).decode('utf-8')

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
