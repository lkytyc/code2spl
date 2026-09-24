class NumberConverter:

    @staticmethod
    def decimal_to_binary(n: int) -> str:
        return bin(n)[2:]

    @staticmethod
    def decimal_to_octal(n: int) -> str:
        return oct(n)[2:]

    @staticmethod
    def decimal_to_hexadecimal(n: int) -> str:
        return hex(n)[2:]

    @staticmethod
    def binary_to_decimal(b: str) -> int:
        return int(b, 2)

    @staticmethod
    def octal_to_decimal(o: str) -> int:
        return int(o, 8)

    @staticmethod
    def hexadecimal_to_decimal(h: str) -> int:
        return int(h, 16)

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
