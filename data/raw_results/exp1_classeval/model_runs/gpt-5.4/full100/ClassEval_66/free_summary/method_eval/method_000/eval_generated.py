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
