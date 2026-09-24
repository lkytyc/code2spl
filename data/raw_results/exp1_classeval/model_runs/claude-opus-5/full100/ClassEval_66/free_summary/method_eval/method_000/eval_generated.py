class NumericEntityUnescaper:

    def replace(self, string):
        out = []
        i = 0
        length = len(string)

        while i < length - 2:
            if string[i] == '&' and string[i + 1] == '#':
                start = i + 2
                is_hex = False

                if string[start] in ('x', 'X'):
                    is_hex = True
                    start += 1

                end = start
                while end < length:
                    c = string[end]
                    if is_hex and not NumericEntityUnescaper.is_hex_char(c):
                        break
                    if not is_hex and not c.isdigit():
                        break
                    end += 1

                if end < length and string[end] == ';':
                    digits = string[start:end]
                    try:
                        code_point = int(digits, 16 if is_hex else 10)
                        out.append(chr(code_point))
                        i = end + 1
                        continue
                    except (ValueError, OverflowError):
                        return ''.join(out)

            out.append(string[i])
            i += 1

        return ''.join(out)

    @staticmethod
    def is_hex_char(c):
        return ('0' <= c <= '9') or ('a' <= c <= 'f') or ('A' <= c <= 'F')

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
