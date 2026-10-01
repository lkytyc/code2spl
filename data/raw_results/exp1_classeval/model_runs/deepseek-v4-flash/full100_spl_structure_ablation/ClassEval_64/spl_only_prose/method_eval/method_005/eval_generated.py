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
