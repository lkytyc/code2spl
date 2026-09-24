class NumberWordFormatter:
    def __init__(self):
        self.digits = [
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
        self.teens = [
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
        self.tens = [
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
        self.more = [
            "",
            "THOUSAND",
            "MILLION",
            "BILLION",
            "TRILLION",
            "QUADRILLION",
            "QUINTILLION",
            "SEXTILLION",
            "SEPTILLION",
            "OCTILLION",
            "NONILLION",
            "DECILLION",
        ]

    def format(self, x):
        if x is None:
            return ""
        return self.format_string(str(x))

    def format_string(self, x):
        s = str(x).strip().upper()
        if not s:
            return ""

        neg = False
        if s.startswith("-"):
            neg = True
            s = s[1:].strip()

        if not s:
            return ""

        if "." in s:
            left, right = s.split(".", 1)
        else:
            left, right = s, ""

        left = "".join(ch for ch in left if ch.isdigit())
        right = "".join(ch for ch in right if ch.isdigit())

        if not left:
            left = "0"

        left = left.lstrip("0") or "0"

        whole_groups = []
        rev = left[::-1]
        for i in range(0, len(rev), 3):
            chunk = rev[i:i + 3][::-1]
            chunk = chunk.zfill(3)
            whole_groups.append(chunk)

        parts = []
        for idx, chunk in enumerate(whole_groups):
            words = self.trans_three(chunk)
            if words:
                scale = self.parse_more(idx)
                if scale:
                    words = f"{words} {scale}"
                parts.append(words)

        whole_text = " ".join(reversed(parts)).strip()

        if whole_text == "":
            whole_text = "ZERO"

        if right:
            cents = right[:2].ljust(2, "0")
            cents_words = self.trans_two(cents)
            if cents_words:
                if whole_text == "ZERO":
                    result = f"ZERO AND CENTS {cents_words} ONLY"
                else:
                    result = f"{whole_text} AND CENTS {cents_words} ONLY"
            else:
                result = f"{whole_text} ONLY"
        else:
            result = f"{whole_text} ONLY"

        if neg and result != "ZERO ONLY":
            result = f"MINUS {result}"

        return result

    def trans_two(self, s):
        s = str(s).strip()
        if not s:
            return ""
        s = "".join(ch for ch in s if ch.isdigit())
        if not s:
            return ""
        s = s[-2:].zfill(2)
        n = int(s)
        if n == 0:
            return ""
        if n < 10:
            return self.digits[n]
        if 10 <= n < 20:
            return self.teens[n - 10]
        ten = n // 10
        one = n % 10
        if one == 0:
            return self.tens[ten]
        return f"{self.tens[ten]} {self.digits[one]}"

    def trans_three(self, s):
        s = str(s).strip()
        s = "".join(ch for ch in s if ch.isdigit())
        if not s:
            return ""
        s = s[-3:].zfill(3)
        n = int(s)
        if n == 0:
            return ""
        h = n // 100
        rest = n % 100
        if h == 0:
            return self.trans_two(f"{rest:02d}")
        hundreds = f"{self.digits[h]} HUNDRED"
        if rest == 0:
            return hundreds
        return f"{hundreds} AND {self.trans_two(f'{rest:02d}')}"

    def parse_more(self, i):
        if i < 0:
            return ""
        if i < len(self.more):
            return self.more[i]
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


class NumberWordFormatterTestTransTwo(unittest.TestCase):
    def test_trans_two_1(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.trans_two("23"), "TWENTY THREE")

    def test_trans_two_2(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.trans_two("10"), "TEN")

    def test_trans_two_3(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.trans_two("05"), "FIVE")

    def test_trans_two_4(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.trans_two("00"), "")

    def test_trans_two_5(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.trans_two("01"), "ONE")

    def test_trans_two_6(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.trans_two("80"), "EIGHTY")


class NumberWordFormatterTestTransThree(unittest.TestCase):
    def test_trans_three_1(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.trans_three("123"), "ONE HUNDRED AND TWENTY THREE")

    def test_trans_three_2(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.trans_three("900"), "NINE HUNDRED")

    def test_trans_three_3(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.trans_three("007"), "SEVEN")

    def test_trans_three_4(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.trans_three("001"), "ONE")

    def test_trans_three_5(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.trans_three("006"), "SIX")


class NumberWordFormatterTestParseMore(unittest.TestCase):
    def test_parse_more_1(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.parse_more(0), "")

    def test_parse_more_2(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.parse_more(1), "THOUSAND")

    def test_parse_more_3(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.parse_more(2), "MILLION")

    def test_parse_more_4(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.parse_more(3), "BILLION")


class NumberWordFormatterTest(unittest.TestCase):
    def test_NumberWordFormatter(self):
        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format(123456),
                         "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY")

        formatter = NumberWordFormatter()
        self.assertEqual(formatter.format_string('123456'),
                         "ONE HUNDRED AND TWENTY THREE THOUSAND FOUR HUNDRED AND FIFTY SIX ONLY")

        formatter = NumberWordFormatter()
        self.assertEqual(formatter.trans_two("23"), "TWENTY THREE")

        formatter = NumberWordFormatter()
        self.assertEqual(formatter.trans_three("123"), "ONE HUNDRED AND TWENTY THREE")

        formatter = NumberWordFormatter()
        self.assertEqual(formatter.parse_more(1), "THOUSAND")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
