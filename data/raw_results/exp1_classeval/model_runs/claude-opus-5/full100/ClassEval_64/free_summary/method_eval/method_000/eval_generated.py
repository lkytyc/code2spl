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
