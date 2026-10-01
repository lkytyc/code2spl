class NumberWordFormatter:
    def __init__(self):
        self.NUMBER = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]
        self.NUMBER_TEEN = ["TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
        self.NUMBER_TEN = ["TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
        self.NUMBER_MORE = ["", "THOUSAND", "MILLION", "BILLION"]
        self.NUMBER_SUFFIX = ["", "k", "w", "m", "b", "t", "p", "e", "", "", "", "", "", "", "", ""]

    def format(self, x):
        if x is not None:
            return self.format_string(str(x))
        return ""

    def format_string(self, x):
        parts = x.split(".", 1)
        lstr = parts[0]
        rstr = parts[1] if len(parts) > 1 else ""
        lstrrev = lstr[::-1]
        a = ["", "", "", "", ""]
        if len(lstrrev) % 3 == 1:
            lstrrev += "00"
        elif len(lstrrev) % 3 == 2:
            lstrrev += "0"
        lm = ""
        for i in range(len(lstrrev) // 3):
            a[i] = lstrrev[3 * i:3 * i + 3][::-1]
            if a[i] != "000":
                lm = self.trans_three(a[i]) + " " + self.parse_more(i) + " " + lm
            else:
                lm = self.trans_three(a[i]) + lm
        xs = "AND CENTS " + self.trans_two(rstr) + " " if rstr else ""
        if not lm.strip():
            return "ZERO ONLY"
        return lm.strip() + " " + xs + "ONLY"

    def parse_more(self, i):
        return self.NUMBER_MORE[i]

    def trans_three(self, s):
        if s[0] == "0":
            return self.trans_two(s[1:])
        if s[1:] == "00":
            return self.NUMBER[int(s[0])] + " HUNDRED"
        return self.NUMBER[int(s[0])] + " HUNDRED AND " + self.trans_two(s[1:])

    def trans_two(self, s):
        s = s.zfill(2)
        if s[0] == "0":
            return self.NUMBER[int(s[-1])]
        elif s[0] == "1":
            return self.NUMBER_TEEN[int(s) - 10]
        elif s[1] == "0":
            return self.NUMBER_TEN[int(s[0]) - 1]
        else:
            return self.NUMBER_TEN[int(s[0]) - 1] + " " + self.NUMBER[int(s[-1])]

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
