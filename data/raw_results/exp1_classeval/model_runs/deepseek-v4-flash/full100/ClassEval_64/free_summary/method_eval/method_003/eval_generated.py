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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
