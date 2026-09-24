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

class NumberConverterTestBinaryToDecimal(unittest.TestCase):
    def test_binary_to_decimal(self):
        self.assertEqual(42423, NumberConverter.binary_to_decimal('1010010110110111'))

    def test_binary_to_decimal_2(self):
        self.assertEqual(10615, NumberConverter.binary_to_decimal('10100101110111'))

    def test_binary_to_decimal_3(self):
        self.assertEqual(42455, NumberConverter.binary_to_decimal('1010010111010111'))

    def test_binary_to_decimal_4(self):
        self.assertEqual(169819, NumberConverter.binary_to_decimal('101001011101011011'))

    def test_binary_to_decimal_5(self):
        self.assertEqual(339639, NumberConverter.binary_to_decimal('1010010111010110111'))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
