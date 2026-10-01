class NumberConverter:
    def binary_to_decimal(self, binary_num):
        try:
            decimal_num = int(binary_num, 2)
        except TypeError:
            raise TypeError("binary_num must be a string, bytes, or bytearray for base-2 conversion.")
        except ValueError:
            raise ValueError("binary_num must contain valid base-2 digits for conversion.")
        return decimal_num

    def decimal_to_binary(self, decimal_num: int) -> str:
        binary_num = bin(decimal_num)[2:]
        return binary_num

    def decimal_to_hex(self, decimal_num: int) -> str:
        hex_num = hex(decimal_num)[2:]
        return hex_num

    def decimal_to_octal(self, decimal_num: int) -> str:
        octal_num = oct(decimal_num)[2:]
        return octal_num

    def hex_to_decimal(self, hex_num):
        decimal_num = int(hex_num, 16)
        return decimal_num

    def octal_to_decimal(self, octal_num: str) -> int:
        decimal_num = int(octal_num, 8)
        return decimal_num

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
