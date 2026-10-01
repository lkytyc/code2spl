class NumberConverter:
    def binary_to_decimal(self, binary_num: str) -> int:
        try:
            decimal_num = int(binary_num, 2)
            return decimal_num
        except ValueError:
            print("Error converting binary_num to integer: invalid binary literal")
            raise ValueError("int(binary_num, 2) fails because binary_num is not a valid base-2 string.")

    def decimal_to_binary(self, decimal_num: int) -> str:
        binary_num = bin(decimal_num)[2:]
        return binary_num

    def decimal_to_hex(self, decimal_num: int) -> str:
        try:
            hex_num = hex(decimal_num)[2:]
            return hex_num
        except TypeError:
            print("TypeError raised by hex() because decimal_num must be integer-compatible.")
            raise TypeError("hex() cannot convert a non-integer-compatible value.")

    def decimal_to_octal(self, decimal_num: int) -> str:
        try:
            octal_num = oct(decimal_num)[2:]
            return octal_num
        except TypeError:
            print("oct() conversion failed because decimal_num is not an integer or an object implementing __index__.")
            raise TypeError("Raised by oct(decimal_num) when decimal_num is not a valid integer type.")

    def hex_to_decimal(self, hex_num: str) -> int:
        try:
            decimal_num = int(hex_num, 16)
            return decimal_num
        except ValueError:
            print("int(hex_num, 16) raised ValueError: invalid literal for int() with base 16")
            raise ValueError("Raised when the hexadecimal string cannot be interpreted as an integer.")
        except TypeError:
            print("int(hex_num, 16) raised TypeError: int() can't convert non-string with explicit base")
            raise TypeError("Raised when the input type is not supported by int() with base 16.")

    def octal_to_decimal(self) -> int:
        try:
            decimal_num = int(self.octal_input, 8)
            return decimal_num
        except ValueError:
            print("ValueError: invalid octal literal")
            raise ValueError("Raised when the input cannot be parsed as a base-8 integer.")
        except TypeError:
            print("TypeError: int() can't convert non-string with explicit base")
            raise TypeError("Raised when the input type is unsupported for explicit base conversion.")

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

class NumberConvertTestMain(unittest.TestCase):
    def test_main(self):
        self.assertEqual('1010010110110111', NumberConverter.decimal_to_binary(42423))
        self.assertEqual(42423, NumberConverter.binary_to_decimal('1010010110110111'))
        self.assertEqual('122667', NumberConverter.decimal_to_octal(42423))
        self.assertEqual('122667', NumberConverter.decimal_to_octal(42423))
        self.assertEqual('a5b7', NumberConverter.decimal_to_hex(42423))
        self.assertEqual(42423, NumberConverter.hex_to_decimal('a5b7'))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
