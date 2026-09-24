class NumericEntityUnescaper:
    def __init__(self):
        pass

    def is_hex_char(self, char):
        return ('0' <= char <= '9') or ('a' <= char <= 'f') or ('A' <= char <= 'F')

    def replace(self, string):
        if string is None:
            return None

        out = []
        i = 0
        n = len(string)

        while i < n:
            ch = string[i]
            if ch != '&' or i + 1 >= n or string[i + 1] != '#':
                out.append(ch)
                i += 1
                continue

            j = i + 2
            base = 10
            if j < n and (string[j] == 'x' or string[j] == 'X'):
                base = 16
                j += 1

            start_digits = j
            if base == 10:
                while j < n and string[j].isdigit():
                    j += 1
            else:
                while j < n and self.is_hex_char(string[j]):
                    j += 1

            if j == start_digits or j >= n or string[j] != ';':
                break

            num_str = string[start_digits:j]
            try:
                codepoint = int(num_str, base)
                out.append(chr(codepoint))
            except Exception:
                break

            i = j + 1

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
