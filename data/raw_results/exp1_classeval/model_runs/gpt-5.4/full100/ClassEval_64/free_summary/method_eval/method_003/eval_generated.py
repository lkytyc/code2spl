class NumberConverter:
    @staticmethod
    def decimal_to_binary(decimal_num):
        return format(decimal_num, 'b')

    @staticmethod
    def binary_to_decimal(binary_num):
        return int(binary_num, 2)

    @staticmethod
    def decimal_to_octal(decimal_num):
        return format(decimal_num, 'o')

    @staticmethod
    def octal_to_decimal(octal_num):
        return int(octal_num, 8)

    @staticmethod
    def decimal_to_hex(decimal_num):
        return format(decimal_num, 'x')

    @staticmethod
    def hex_to_decimal(hex_num):
        return int(hex_num, 16)

import unittest

class NumberConvertTestOctalToDecimal(unittest.TestCase):
    def test_octal_to_decimal(self):
        self.assertEqual(42423, NumberConverter.octal_to_decimal('122667'))

    def test_octal_to_decimal_2(self):
        self.assertEqual(21271, NumberConverter.octal_to_decimal('51427'))

    def test_octal_to_decimal_3(self):
        self.assertEqual(84907, NumberConverter.octal_to_decimal('245653'))

    def test_octal_to_decimal_4(self):
        self.assertEqual(169815, NumberConverter.octal_to_decimal('513527'))

    def test_octal_to_decimal_5(self):
        self.assertEqual(339630, NumberConverter.octal_to_decimal('1227256'))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
