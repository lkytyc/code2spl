class NumericEntityUnescaper:
    def is_hex_char(self, char):
        return char.isdigit() or ('a' <= char.lower() <= 'f')

    def replace(self, string):
        if string is None:
            return None

        result = []
        i = 0
        length = len(string)

        while i < length - 2:
            if string[i] == '&' and string[i + 1] == '#':
                start = i + 2
                if start >= length:
                    return ''.join(result)

                is_hex = False
                if string[start] == 'x' or string[start] == 'X':
                    is_hex = True
                    start += 1
                    if start >= length:
                        return ''.join(result)

                end = start
                while end < length and self.is_hex_char(string[end]):
                    end += 1

                if end >= length:
                    return ''.join(result)

                if end > start and string[end] == ';':
                    num_text = string[start:end]
                    try:
                        value = int(num_text, 16 if is_hex else 10)
                        result.append(chr(value))
                        i = end + 1
                        continue
                    except Exception:
                        return ''.join(result)

            result.append(string[i])
            i += 1

        return ''.join(result)

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
