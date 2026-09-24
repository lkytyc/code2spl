class NumberConverter:
    @staticmethod
    def decimal_to_binary(value):
        return format(int(value), 'b')

    @staticmethod
    def decimal_to_octal(value):
        return format(int(value), 'o')

    @staticmethod
    def decimal_to_hex(value):
        return format(int(value), 'x')

    @staticmethod
    def binary_to_decimal(value):
        s = str(value).strip()
        sign = ''
        if s and s[0] in '+-':
            sign = s[0]
            s = s[1:].strip()
        if s.lower().startswith('0b'):
            s = s[2:]
        return int(sign + s, 2)

    @staticmethod
    def octal_to_decimal(value):
        s = str(value).strip()
        sign = ''
        if s and s[0] in '+-':
            sign = s[0]
            s = s[1:].strip()
        if s.lower().startswith('0o'):
            s = s[2:]
        return int(sign + s, 8)

    @staticmethod
    def hex_to_decimal(value):
        s = str(value).strip()
        sign = ''
        if s and s[0] in '+-':
            sign = s[0]
            s = s[1:].strip()
        if s.lower().startswith('0x'):
            s = s[2:]
        return int(sign + s, 16)

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
