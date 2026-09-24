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
        if isinstance(x, str):
            return self.format_string(x)

        if isinstance(x, int):
            return self.format_string(str(x))

        if isinstance(x, float):
            s = format(x, "f").rstrip("0").rstrip(".")
            if s == "-0":
                s = "0"
            return self.format_string(s)

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
        s = str(x).strip()
        if not s:
            return "ZERO ONLY"

        negative = False
        if s[0] == "-":
            negative = True
            s = s[1:].strip()
        elif s[0] == "+":
            s = s[1:].strip()

        s = s.replace(",", "")
        if not s:
            return "ZERO ONLY"

        if "." in s:
            int_part, dec_part = s.split(".", 1)
        else:
            int_part, dec_part = s, ""

        int_part = int_part if int_part else "0"
        if int_part.isdigit():
            int_part = str(int(int_part))
        else:
            raise ValueError("Invalid number string")

        if dec_part and not dec_part.isdigit():
            raise ValueError("Invalid number string")

        int_words = []
        if int(int_part) == 0:
            int_words.append("ZERO")
        else:
            groups = []
            temp = int_part
            while temp:
                groups.append(temp[-3:])
                temp = temp[:-3]

            for i in range(len(groups) - 1, -1, -1):
                group = groups[i].zfill(3)
                if int(group) == 0:
                    continue
                part = self.trans_three(group)
                more = self.parse_more(i)
                if more:
                    int_words.append(part + " " + more)
                else:
                    int_words.append(part)

        result = " ".join(int_words).strip()

        dec_part = dec_part.rstrip("0")
        if dec_part:
            dec_words = []
            for ch in dec_part:
                dec_words.append("ZERO" if ch == "0" else self.NUMBER[int(ch)])
            result = (result + " POINT " + " ".join(dec_words)).strip()

        if negative:
            result = "MINUS " + result

        return result + " ONLY"

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
        ten = int(s[0])
        one = int(s[1])
        if one == 0:
            return self.NUMBER_TEN[ten - 1]
        return self.NUMBER_TEN[ten - 1] + " " + self.NUMBER[one]

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
        hundred = int(s[0])
        rest = s[1:]
        rest_num = int(rest)

        parts = []
        if hundred > 0:
            parts.append(self.NUMBER[hundred] + " HUNDRED")
            if rest_num > 0:
                parts.append("AND " + self.trans_two(rest))
        else:
            if rest_num > 0:
                parts.append(self.trans_two(rest))

        return " ".join(parts).strip()

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

class NumberWordFormatterTestFormat(unittest.TestCase):
    def test_format_1(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format(123456),
                         "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY")

    def test_format_2(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format(1000), "ONE THOUSAND ONLY")

    def test_format_3(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format(1000000), "ONE MILLION ONLY")

    def test_format_4(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format(1.23), "ONE AND CENTS TWENTY THREE ONLY")

    def test_format_5(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format(0), "ZERO ONLY")

    def test_format_6(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format(None), "")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
