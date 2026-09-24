class NumberWordFormatter:
    """
    This is a class that provides to convert numbers into their corresponding English word representation, including handling the conversion of both the integer and decimal parts, and incorporating appropriate connectors and units.
    """

    def __init__(self):
        """
        Initialize NumberWordFormatter object.
        """
        self.NUMBER = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
        self.NUMBER_TEEN = ["TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN",
                            "EIGHTEEN",
                            "NINETEEN"]
        self.NUMBER_TEN = ["TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
        self.NUMBER_MORE = ["", "THOUSAND", "MILLION", "BILLION"]
        self.NUMBER_SUFFIX = ["k", "w", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e"]

    def format(self, x):
        """
        Converts a number into words format
        :param x: int or float, the number to be converted into words format
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.format(123456)
        "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY"
        """
        return self.format_string(str(x))

    def format_string(self, x):
        """
        Converts a string representation of a number into words format
        :param x: str, the string representation of a number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.format_string("123456")
        "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY"
        """
        s = str(x).strip().upper()
        if not s:
            return "ONLY"
        if s.startswith("+"):
            s = s[1:]
        if s.startswith("-"):
            return "MINUS " + self.format_string(s[1:])
        if "." in s:
            int_part, dec_part = s.split(".", 1)
        else:
            int_part, dec_part = s, ""
        int_part = int_part.lstrip("0") or "0"
        if not int_part.isdigit() or (dec_part and not dec_part.isdigit()):
            raise ValueError("Invalid number string")
        if int(int_part) == 0 and not dec_part:
            return "ZERO ONLY"
        groups = []
        while int_part:
            groups.append(int_part[-3:])
            int_part = int_part[:-3]
        parts = []
        for i, g in enumerate(groups):
            if int(g) == 0:
                continue
            words = self.trans_three(g.zfill(3)) if len(g) < 3 else self.trans_three(g)
            suffix = self.parse_more(i)
            if suffix:
                parts.append(words + " " + suffix)
            else:
                parts.append(words)
        parts = list(reversed(parts))
        result = " ".join(parts).strip()
        if dec_part:
            dec_words = []
            for ch in dec_part:
                dec_words.append(self.NUMBER[int(ch)])
            dec_words = [w for w in dec_words if w]
            if dec_words:
                result = (result + " POINT " + " ".join(dec_words)).strip()
        return (result + " ONLY").strip()

    def trans_two(self, s):
        """
        Converts a two-digit number into words format
        :param s: str, the two-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_two("23")
        "TWENTY THREE"
        """
        s = str(s).zfill(2)[-2:]
        n = int(s)
        if n == 0:
            return ""
        if n < 10:
            return self.NUMBER[n]
        if 10 <= n < 20:
            return self.NUMBER_TEEN[n - 10]
        tens = n // 10
        ones = n % 10
        if ones == 0:
            return self.NUMBER_TEN[tens - 1]
        return self.NUMBER_TEN[tens - 1] + " " + self.NUMBER[ones]

    def trans_three(self, s):
        """
        Converts a three-digit number into words format
        :param s: str, the three-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_three("123")
        "ONE HUNDRED AND TWENTY THREE"
        """
        s = str(s).zfill(3)[-3:]
        n = int(s)
        if n == 0:
            return ""
        hundreds = n // 100
        rem = n % 100
        parts = []
        if hundreds:
            parts.append(self.NUMBER[hundreds] + " HUNDRED")
            if rem:
                parts.append("AND")
        if rem:
            parts.append(self.trans_two(str(rem).zfill(2)))
        return " ".join(parts)

    def parse_more(self, i):
        """
        Parses the thousand/million/billion suffix based on the index
        :param i: int, the index representing the magnitude (thousand, million, billion)
        :return: str, the corresponding suffix for the magnitude
        >>> formatter = NumberWordFormatter()
        >>> formatter.parse_more(1)
        "THOUSAND"
        """
        if 0 <= i < len(self.NUMBER_MORE):
            return self.NUMBER_MORE[i]
        return ""

import unittest

class NumberWordFormatterTestFormatString(unittest.TestCase):
    def test_format_string_1(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format_string('123456'),
                         "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY")

    def test_format_string_2(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format_string('1000'), "ONE THOUSAND ONLY")

    def test_format_string_3(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format_string('1000000'), "ONE MILLION ONLY")

    def test_format_string_4(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format_string('1.23'), "ONE AND CENTS TWENTY THREE ONLY")

    def test_format_string_5(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format_string('0'), "ZERO ONLY")

    def test_format_string_6(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format_string('10'), "TEN ONLY")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
