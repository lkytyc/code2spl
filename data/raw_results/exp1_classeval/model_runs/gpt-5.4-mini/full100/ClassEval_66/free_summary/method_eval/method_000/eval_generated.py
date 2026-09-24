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

class NumericEntityUnescaperTestReplace(unittest.TestCase):
    def test_replace_1(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.replace("&#65;&#66;&#67;")
        self.assertEqual(res, "ABC")

    def test_replace_2(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.replace("&#65;&#65;&#65;")
        self.assertEqual(res, "AAA")

    def test_replace_3(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.replace("&#66;&#66;&#66;")
        self.assertEqual(res, "BBB")

    def test_replace_4(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.replace("&#67;&#67;&#67;")
        self.assertEqual(res, "CCC")

    def test_replace_5(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.replace("")
        self.assertEqual(res, "")

    def test_replace_6(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.replace("&#")
        self.assertEqual(res, "")

    def test_replace_7(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.replace("&#X65;&#66;&#67;")
        self.assertEqual(res, "eBC")

    def test_replace_8(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.replace("&#???;&#66;&#67;")
        self.assertEqual(res, "&#???;BC")

    def test_replace_9(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.replace("&#67;&#67;&#67;;")
        self.assertEqual(res, "CCC")

    def test_replace_10(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.replace("&#X")
        self.assertEqual(res, "")

    def test_replace_11(self):
        unescaper = NumericEntityUnescaper()
        res = unescaper.replace("&#c1d;&#66;&#67;")
        self.assertEqual(res, "")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
