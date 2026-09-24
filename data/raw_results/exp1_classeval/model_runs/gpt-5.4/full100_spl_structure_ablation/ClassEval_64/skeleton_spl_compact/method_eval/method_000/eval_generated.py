class NumberConverter:
    """
    The class allows to convert decimal to binary, octal and hexadecimal
    respectively and contrarily.
    """

    @staticmethod
    def decimal_to_binary(decimal_num):
        """
        Convert a number from decimal format to binary format.
        :param decimal_num: int, decimal number
        :return: str, the binary representation of an integer.
        """
        binary_num = bin(decimal_num)[2:]
        return binary_num

    @staticmethod
    def binary_to_decimal(binary_num):
        """
        Convert a number from binary format to decimal format.
        :param binary_num: str, binary number
        :return: int, the decimal representation of binary number str.
        """
        decimal_num = int(binary_num, 2)
        return decimal_num

    @staticmethod
    def decimal_to_octal(decimal_num):
        """
        Convert a number from decimal format to octal format.
        :param decimal_num: int, decimal number
        :return: str, the octal representation of an integer.
        """
        octal_num = oct(decimal_num)[2:]
        return octal_num

    @staticmethod
    def octal_to_decimal(octal_num):
        """
        Convert a number from octal format to decimal format.
        :param octal_num: str, octal num
        :return: int, the decimal representation of octal number str.
        """
        decimal_num = int(octal_num, 8)
        return decimal_num

    @staticmethod
    def decimal_to_hex(decimal_num):
        """
        Convert a number from decimal format to hex format.
        :param decimal_num: int, decimal number
        :return: str, the hex representation of an integer.
        """
        hex_value = hex(decimal_num)
        hex_num = hex_value[2:]
        return hex_num

    @staticmethod
    def hex_to_decimal(hex_num):
        """
        Convert a number from hex format to decimal format.
        :param hex_num: str, hex num
        :return: int, the decimal representation of hex number str.
        """
        decimal_num = int(hex_num, 16)
        return decimal_num

import unittest

class NumberConverterTestDecimalToBinary(unittest.TestCase):
    def test_decimal_to_binary(self):
        self.assertEqual('1010010110110111', NumberConverter.decimal_to_binary(42423))

    def test_decimal_to_binary_2(self):
        self.assertEqual('101001100010111', NumberConverter.decimal_to_binary(21271))

    def test_decimal_to_binary_3(self):
        self.assertEqual('1010010111010111', NumberConverter.decimal_to_binary(42455))

    def test_decimal_to_binary_4(self):
        self.assertEqual('10100101110101011', NumberConverter.decimal_to_binary(84907))

    def test_decimal_to_binary_5(self):
        self.assertEqual('101001011101010111', NumberConverter.decimal_to_binary(169815))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
