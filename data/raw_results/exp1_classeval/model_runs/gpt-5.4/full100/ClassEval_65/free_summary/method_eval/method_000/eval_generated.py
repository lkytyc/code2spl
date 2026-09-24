class NumberWordFormatter:
    def __init__(self):
        self.NUMBER_SINGLES = [
            "",
            "ONE",
            "TWO",
            "THREE",
            "FOUR",
            "FIVE",
            "SIX",
            "SEVEN",
            "EIGHT",
            "NINE",
        ]
        self.NUMBER_TEENS = [
            "TEN",
            "ELEVEN",
            "TWELVE",
            "THIRTEEN",
            "FOURTEEN",
            "FIFTEEN",
            "SIXTEEN",
            "SEVENTEEN",
            "EIGHTEEN",
            "NINETEEN",
        ]
        self.NUMBER_TENS = [
            "",
            "",
            "TWENTY",
            "THIRTY",
            "FORTY",
            "FIFTY",
            "SIXTY",
            "SEVENTY",
            "EIGHTY",
            "NINETY",
        ]
        self.NUMBER_MORE = [
            "",
            "THOUSAND",
            "MILLION",
            "BILLION",
        ]
        self.NUMBER_SUFFIX = ["", "K", "M", "B", "T"]

    def format(self, x):
        if x is None:
            return ""
        return self.format_string(str(x))

    def format_string(self, x):
        if x is None:
            return ""

        x = str(x).strip().upper()
        if x == "":
            return "ZERO ONLY"

        parts = x.split(".", 1)
        left = parts[0].strip() if len(parts) > 0 else ""
        right = parts[1].strip() if len(parts) > 1 else None

        if left == "":
            left = "0"

        if left.startswith("+"):
            left = left[1:]
        elif left.startswith("-"):
            left = left[1:]

        if not left.isdigit():
            left = "".join(ch for ch in left if ch.isdigit())
            if left == "":
                left = "0"

        groups = [""] * 5
        idx = 0
        p = len(left)
        while p > 0 and idx < 5:
            start = max(0, p - 3)
            groups[idx] = left[start:p]
            p = start
            idx += 1

        words = []
        for i in range(idx - 1, -1, -1):
            grp = groups[i]
            if grp and int(grp) != 0:
                part = self.trans_three(grp)
                scale = self.parse_more(i)
                if scale:
                    words.append(part + " " + scale)
                else:
                    words.append(part)

        result = " ".join(words).strip()

        if result == "":
            result = "ZERO"

        if right is not None and right != "":
            cents = self.trans_two(right)
            if cents != "":
                result = result + " AND CENTS " + cents

        return (result + " ONLY").strip().upper()

    def trans_two(self, s):
        if s is None:
            return ""

        s = str(s).strip()
        digits = "".join(ch for ch in s if ch.isdigit())

        if digits == "":
            return ""

        if len(digits) == 1:
            digits = "0" + digits
        else:
            digits = digits[-2:]

        n = int(digits)
        if n == 0:
            return ""

        if n < 10:
            return self.NUMBER_SINGLES[n]
        if 10 <= n <= 19:
            return self.NUMBER_TEENS[n - 10]

        tens = int(digits[0])
        ones = int(digits[1])

        if ones == 0:
            return self.NUMBER_TENS[tens]
        return self.NUMBER_TENS[tens] + " " + self.NUMBER_SINGLES[ones]

    def trans_three(self, s):
        if s is None:
            return ""

        s = str(s).strip()
        digits = "".join(ch for ch in s if ch.isdigit())

        if digits == "":
            return ""

        digits = digits.zfill(3)[-3:]
        hundreds = int(digits[0])
        last_two = digits[1:]

        if hundreds == 0:
            return self.trans_two(last_two)

        hundred_word = self.NUMBER_SINGLES[hundreds] + " HUNDRED"

        if int(last_two) == 0:
            return hundred_word

        return hundred_word + " AND " + self.trans_two(last_two)

    def parse_more(self, i):
        if i == 0:
            return ""
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
