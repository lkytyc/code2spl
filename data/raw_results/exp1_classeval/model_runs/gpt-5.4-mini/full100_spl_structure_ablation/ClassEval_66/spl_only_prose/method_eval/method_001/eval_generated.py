class NumericEntityUnescaper:
    def __init__(self):
        return

    @staticmethod
    def is_hex_char(char: str) -> bool:
        is_digit = char.isdigit()
        if is_digit:
            return True
        is_hex_letter = char.lower() >= 'a' and char.lower() <= 'f'
        return is_hex_letter

    def replace(self, string: str) -> str:
        out = []
        pos = 0
        length = len(string)

        while pos < length - 2:
            if string[pos] == '&' and string[pos + 1] == '#':
                start = pos + 2
                hexadecimal = False
                if start < length and (string[start] == 'x' or string[start] == 'X'):
                    start += 1
                    hexadecimal = True

                if start == length:
                    return ''.join(out)

                end = start
                while end < length and self.is_hex_char(string[end]):
                    end += 1

                if end < length and string[end] == ';':
                    try:
                        entity_value = int(string[start:end], 16 if hexadecimal else 10)
                    except ValueError:
                        pass
                    else:
                        out.append(chr(entity_value))
                        pos = end + 1
                        continue

            out.append(string[pos])
            pos += 1

        while pos < length:
            out.append(string[pos])
            pos += 1

        return ''.join(out)

import unittest

class NumericEntityUnescaperTestIsHexChar(unittest.TestCase):
    def test_is_hex_char_1(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.is_hex_char('0')
        self.assertEqual(res, True)

    def test_is_hex_char_2(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.is_hex_char('F')
        self.assertEqual(res, True)

    def test_is_hex_char_3(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.is_hex_char('G')
        self.assertEqual(res, False)

    def test_is_hex_char_4(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.is_hex_char('X')
        self.assertEqual(res, False)

    def test_is_hex_char_5(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.is_hex_char('Z')
        self.assertEqual(res, False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
