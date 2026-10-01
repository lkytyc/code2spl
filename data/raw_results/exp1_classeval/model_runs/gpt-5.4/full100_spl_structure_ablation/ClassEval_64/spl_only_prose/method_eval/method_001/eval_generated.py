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
