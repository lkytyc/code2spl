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

class NumberConvertTestHexToDecimal(unittest.TestCase):
    def test_hex_to_decimal(self):
        self.assertEqual(42423, NumberConverter.hex_to_decimal('a5b7'))

    def test_hex_to_decimal_2(self):
        self.assertEqual(21207, NumberConverter.hex_to_decimal('52d7'))

    def test_hex_to_decimal_3(self):
        self.assertEqual(84627, NumberConverter.hex_to_decimal('14a93'))

    def test_hex_to_decimal_4(self):
        self.assertEqual(170615, NumberConverter.hex_to_decimal('29a77'))

    def test_hex_to_decimal_5(self):
        self.assertEqual(342647, NumberConverter.hex_to_decimal('53a77'))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
