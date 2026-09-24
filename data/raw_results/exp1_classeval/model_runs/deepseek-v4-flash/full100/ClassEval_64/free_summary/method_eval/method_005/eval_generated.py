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
