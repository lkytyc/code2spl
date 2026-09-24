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
        if x is None:
            return ""
        if isinstance(x, float):
            integer_part = int(x)
            decimal_part = str(x).split('.')[1] if '.' in str(x) else ''
            result = self.format_string(str(integer_part))
            if decimal_part:
                result += " POINT " + " ".join(self.NUMBER[int(d)] for d in decimal_part)
            return result + " ONLY"
        else:
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
        if x is None or x == "":
            return ""
        x = str(x)
        if x.startswith('-'):
            return "MINUS " + self.format_string(x[1:])
        if '.' in x:
            integer_part, decimal_part = x.split('.')
            result = self.format_string(integer_part)
            if decimal_part:
                result += " POINT " + " ".join(self.NUMBER[int(d)] for d in decimal_part)
            return result + " ONLY"
        # Remove leading zeros
        x = x.lstrip('0')
        if x == "":
            return "ZERO ONLY"
        # Split into groups of three from right
        groups = []
        while len(x) > 3:
            groups.insert(0, x[-3:])
            x = x[:-3]
        groups.insert(0, x)
        result_parts = []
        group_count = len(groups)
        for i, group in enumerate(groups):
            if group == "000":
                continue
            group_str = self.trans_three(group)
            if group_str:
                magnitude_index = group_count - 1 - i
                if magnitude_index > 0:
                    group_str += " " + self.NUMBER_MORE[magnitude_index]
                result_parts.append(group_str)
        if not result_parts:
            return "ZERO ONLY"
        return " ".join(result_parts) + " ONLY"

    def trans_two(self, s):
        """
        Converts a two-digit number into words format
        :param s: str, the two-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_two("23")
        "TWENTY THREE"
        """
        if len(s) == 1:
            return self.NUMBER[int(s)]
        if s[0] == '0':
            return self.NUMBER[int(s[1])]
        if s[0] == '1':
            return self.NUMBER_TEEN[int(s[1])]
        tens = self.NUMBER_TEN[int(s[0]) - 1]
        ones = self.NUMBER[int(s[1])]
        if ones:
            return tens + " " + ones
        return tens

    def trans_three(self, s):
        """
        Converts a three-digit number into words format
        :param s: str, the three-digit number
        :return: str, the number in words format
        >>> formatter = NumberWordFormatter()
        >>> formatter.trans_three("123")
        "ONE HUNDRED AND TWENTY THREE"
        """
        s = s.zfill(3)
        hundreds = int(s[0])
        tens_ones = s[1:]
        result = ""
        if hundreds > 0:
            result += self.NUMBER[hundreds] + " HUNDRED"
            if tens_ones != "00":
                result += " AND "
        if tens_ones != "00":
            result += self.trans_two(tens_ones)
        return result

    def parse_more(self, i):
        """
        Parses the thousand/million/billion suffix based on the index
        :param i: int, the index representing the magnitude (thousand, million, billion)
        :return: str, the corresponding suffix for the magnitude
        >>> formatter = NumberWordFormatter()
        >>> formatter.parse_more(1)
        "THOUSAND"
        """
        if i < len(self.NUMBER_MORE):
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
