class NumberConverter:
    """
    The class allows to convert  decimal to binary, octal and hexadecimal repectively and contrarily
    """

    @staticmethod
    def decimal_to_binary(decimal_num):
        """
        Convert a number from decimal format to binary format.
        :param decimal_num: int, decimal number
        :return: str, the binary representation of an integer.
        >>> NumberConverter.decimal_to_binary(42423)
        '1010010110110111'
        """
        return format(decimal_num, 'b')

    @staticmethod
    def binary_to_decimal(binary_num):
        """
        Convert a number from binary format to decimal format.
        :param binary_num: str, binary number
        :return: int, the decimal representation of binary number str.
        >>> NumberConverter.binary_to_decimal('1010010110110111')
        42423
        """
        return int(binary_num, 2)

    @staticmethod
    def decimal_to_octal(decimal_num):
        """
        Convert a number from decimal format to octal format.
        :param decimal_num: int, decimal number
        :return: str, the octal representation of an integer.
        >>> NumberConverter.decimal_to_octal(42423)
        '122667'
        """
        return format(decimal_num, 'o')

    @staticmethod
    def octal_to_decimal(octal_num):
        """
        Convert a number from octal format to decimal format.
        :param octal_num: str, octal num
        :return: int, the decimal representation of octal number str.
        >>> NumberConverter.octal_to_decimal('122667')
        42423
        """
        return int(octal_num, 8)

    @staticmethod
    def decimal_to_hex(decimal_num):
        """
        Convert a number from decimal format to hex format.
        :param decimal_num: int, decimal number
        :return hex_num: str, the hex representation of an integer.
        >>> NumberConverter.decimal_to_hex(42423)
        'a5b7'
        """
        return format(decimal_num, 'x')

    @staticmethod
    def hex_to_decimal(hex_num):
        """
        Convert a number from hex format to decimal format.
        :param hex_num: str, hex num
        :return: int, the decimal representation of hex number str.
        >>> NumberConverter.hex_to_decimal('a5b7')
        42423
        """
        return int(hex_num, 16)

import unittest

class NumberConvertTestDecimalToOctal(unittest.TestCase):
    def test_decimal_to_octal(self):
        self.assertEqual('122667', NumberConverter.decimal_to_octal(42423))

    def test_decimal_to_octal_2(self):
        self.assertEqual('51427', NumberConverter.decimal_to_octal(21271))

    def test_decimal_to_octal_3(self):
        self.assertEqual('245653', NumberConverter.decimal_to_octal(84907))

    def test_decimal_to_octal_4(self):
        self.assertEqual('513527', NumberConverter.decimal_to_octal(169815))

    def test_decimal_to_octal_5(self):
        self.assertEqual('1227256', NumberConverter.decimal_to_octal(339630))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
