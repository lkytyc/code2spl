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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
