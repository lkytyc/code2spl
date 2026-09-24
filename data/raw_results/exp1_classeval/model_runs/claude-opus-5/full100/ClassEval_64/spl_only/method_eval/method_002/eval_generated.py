class NumberConverter:

    def decimal_to_binary(self, decimal_num):
        bin_string = bin(decimal_num)
        binary_num = bin_string[2:]
        return binary_num

    def binary_to_decimal(self, binary_num):
        decimal_num = int(binary_num, 2)
        return decimal_num

    def decimal_to_octal(self, decimal_num):
        oct_string = oct(decimal_num)
        octal_num = oct_string[2:]
        return octal_num

    def octal_to_decimal(self, octal_num):
        decimal_num = int(octal_num, 8)
        return decimal_num

    def decimal_to_hex(self, decimal_num):
        hex_string_with_prefix = hex(decimal_num)
        hex_num = hex_string_with_prefix[2:]
        return hex_num

    def hex_to_decimal(self, hex_num):
        decimal_num = int(hex_num, 16)
        return decimal_num

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
