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
