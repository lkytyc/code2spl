class NumberConverter:
    def binary_to_decimal(self):
        try:
            decimal_num = int(self.binary_num, 2)
        except ValueError:
            raise
        return decimal_num

    def decimal_to_binary(self, decimal_num):
        binary_num = bin(decimal_num)[2:]
        return binary_num

    def decimal_to_hex(self, decimal_num):
        hex_value = hex(decimal_num)
        hex_num = hex_value[2:]
        return hex_num

    def decimal_to_octal(self, decimal_num):
        octal_num = oct(decimal_num)[2:]
        return octal_num

    def hex_to_decimal(self, hex_num):
        try:
            decimal_num = int(hex_num, 16)
        except ValueError:
            raise
        return decimal_num

    def octal_to_decimal(self):
        decimal_num = int(self.octal_num, 8)
        return decimal_num

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
