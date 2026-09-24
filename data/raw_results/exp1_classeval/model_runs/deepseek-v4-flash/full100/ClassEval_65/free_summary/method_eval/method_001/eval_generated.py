class NumberWordFormatter:
    def __init__(self):
        self.ones = ["", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN"]
        self.tens = ["", "", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY"]
        self.scale = ["", "THOUSAND", "MILLION", "BILLION", "TRILLION", "QUADRILLION", "QUINTILLION"]

    def format(self, value):
        if value is None:
            return ""
        return self.format_string(str(value))

    def format_string(self, value_str):
        if "." in value_str:
            int_part, dec_part = value_str.split(".", 1)
        else:
            int_part, dec_part = value_str, ""
        int_part = int_part.strip()
        dec_part = dec_part.strip()
        if int_part == "" or int_part.replace(",", "").replace(" ", "") == "0" or all(c == '0' for c in int_part.replace(",", "")):
            return "ZERO ONLY"
        # Remove commas and spaces
        int_part_clean = int_part.replace(",", "").replace(" ", "")
        # Group into threes from right
        groups = []
        while len(int_part_clean) > 3:
            groups.insert(0, int_part_clean[-3:])
            int_part_clean = int_part_clean[:-3]
        if int_part_clean:
            groups.insert(0, int_part_clean)
        # Convert each group
        words = []
        group_count = len(groups)
        for i, group in enumerate(groups):
            if int(group) == 0:
                continue
            group_words = self.trans_three(group)
            scale_index = group_count - 1 - i
            if scale_index > 0:
                group_words += " " + self.parse_more(scale_index)
            words.append(group_words)
        result = " ".join(words)
        # Decimal part
        if dec_part:
            # Take first two digits for cents
            cents = dec_part[:2]
            if cents == "":
                cents = "0"
            cents_int = int(cents)
            if cents_int > 0:
                cents_words = self.trans_two(cents)
                result += " AND CENTS " + cents_words
        result += " ONLY"
        return result

    def trans_three(self, three_str):
        if len(three_str) == 1:
            return self.ones[int(three_str)]
        elif len(three_str) == 2:
            return self.trans_two(three_str)
        else:
            hundreds = int(three_str[0])
            rest = three_str[1:]
            parts = []
            if hundreds > 0:
                parts.append(self.ones[hundreds] + " HUNDRED")
            if int(rest) > 0:
                if parts:
                    parts.append("AND")
                parts.append(self.trans_two(rest))
            return " ".join(parts)

    def trans_two(self, two_str):
        if len(two_str) == 1:
            return self.ones[int(two_str)]
        num = int(two_str)
        if num < 20:
            return self.ones[num]
        else:
            tens_digit = num // 10
            ones_digit = num % 10
            if ones_digit == 0:
                return self.tens[tens_digit]
            else:
                return self.tens[tens_digit] + " " + self.ones[ones_digit]

    def parse_more(self, index):
        if index < len(self.scale):
            return self.scale[index]
        else:
            # For larger numbers, just return empty or extend
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
