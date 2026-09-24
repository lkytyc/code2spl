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
