class NumericEntityUnescaper:
    def __init__(self):
        pass

    def replace(self, string):
        out = []
        pos = 0
        length = len(string)

        while pos < length - 2:
            if string[pos:pos + 2] != "&#":
                out.append(string[pos])
                pos += 1
                continue

            start = pos + 2
            is_hex = False

            if start < length and string[start] in ("x", "X"):
                start += 1
                is_hex = True

            if start == length:
                return "".join(out)

            end = start
            while end < length and self.is_hex_char(string[end]):
                end += 1

            if end < length and string[end] == ";":
                try:
                    entity_value = int(string[start:end], 16 if is_hex else 10)
                except ValueError:
                    return "".join(out)

                out.append(chr(entity_value))
                pos = end + 1
                continue

            break

        return "".join(out)

    def is_hex_char(self, char):
        if char.isdigit():
            return True
        lower_char = char.lower()
        return 'a' <= lower_char <= 'f'

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
