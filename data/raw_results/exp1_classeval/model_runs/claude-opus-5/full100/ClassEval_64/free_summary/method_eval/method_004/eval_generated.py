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

class NumberConvertTestDecimalToHex(unittest.TestCase):
    def test_decimal_to_hex(self):
        self.assertEqual('a5b7', NumberConverter.decimal_to_hex(42423))

    def test_decimal_to_hex_2(self):
        self.assertEqual('5317', NumberConverter.decimal_to_hex(21271))

    def test_decimal_to_hex_3(self):
        self.assertEqual('14bab', NumberConverter.decimal_to_hex(84907))

    def test_decimal_to_hex_4(self):
        self.assertEqual('29757', NumberConverter.decimal_to_hex(169815))

    def test_decimal_to_hex_5(self):
        self.assertEqual('52eb7', NumberConverter.decimal_to_hex(339639))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
