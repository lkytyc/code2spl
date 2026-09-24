class NumberConverter:
    def decimal_to_binary(self, decimal_num: int) -> str:
        binary_num = bin(decimal_num)[2:]
        return binary_num

    def binary_to_decimal(self, binary_num):
        decimal_num = int(binary_num, 2)
        return decimal_num

    def decimal_to_octal(self, decimal_num: int) -> str:
        octal_num = oct(decimal_num)[2:]
        return octal_num

    def octal_to_decimal(self, octal_num: str) -> int:
        decimal_num = int(octal_num, 8)
        return decimal_num

    def decimal_to_hex(self, decimal_num: int) -> str:
        hex_num = hex(decimal_num)[2:]
        return hex_num

    def hex_to_decimal(self, hex_num) -> int:
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
