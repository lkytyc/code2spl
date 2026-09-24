class NumericEntityUnescaper:
    """
    This is a class that provides functionality to replace numeric entities with their corresponding characters in a given string.
    """

    def __init__(self):
        pass

    def replace(self, string):
        """
        Replaces numeric character references (HTML entities) in the input string with their corresponding Unicode characters.
        :param string: str, the input string containing numeric character references.
        :return: str, the input string with numeric character references replaced with their corresponding Unicode characters.
        >>> unescaper = NumericEntityUnescaper()
        >>> unescaper.replace("&#65;&#66;&#67;")
        'ABC'

        """
        out = []
        i = 0
        length = len(string)
        while i < length:
            if string[i] == '&' and i + 2 < length and string[i + 1] == '#':
                j = i + 2
                if j < length and string[j] in ('x', 'X'):
                    j += 1
                    start = j
                    while j < length and self.is_hex_char(string[j]):
                        j += 1
                    if j > start and j < length and string[j] == ';':
                        try:
                            code_point = int(string[start:j], 16)
                            out.append(chr(code_point))
                            i = j + 1
                            continue
                        except (ValueError, OverflowError):
                            pass
                else:
                    start = j
                    while j < length and string[j].isdigit():
                        j += 1
                    if j > start and j < length and string[j] == ';':
                        try:
                            code_point = int(string[start:j])
                            out.append(chr(code_point))
                            i = j + 1
                            continue
                        except (ValueError, OverflowError):
                            pass
            out.append(string[i])
            i += 1
        return ''.join(out)

    @staticmethod
    def is_hex_char(char):
        """
        Determines whether a given character is a hexadecimal digit.
        :param char: str, the character to check.
        :return: bool, True if the character is a hexadecimal digit, False otherwise.
        >>> NumericEntityUnescaper.is_hex_char('a')
        True

        """
        return char.lower() in '0123456789abcdef'

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
