class NumberWordFormatter:
    def __init__(self):
        self.SINGLE_DIGITS = [
            'ZERO', 'ONE', 'TWO', 'THREE', 'FOUR',
            'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE'
        ]
        self.TEENS = [
            'TEN', 'ELEVEN', 'TWELVE', 'THIRTEEN', 'FOURTEEN',
            'FIFTEEN', 'SIXTEEN', 'SEVENTEEN', 'EIGHTEEN', 'NINETEEN'
        ]
        self.TENS = [
            '', '', 'TWENTY', 'THIRTY', 'FORTY', 'FIFTY',
            'SIXTY', 'SEVENTY', 'EIGHTY', 'NINETY'
        ]
        self.MAGNITUDES = ['', 'THOUSAND', 'MILLION', 'BILLION']
        # Dead code: left over from a different formatting path
        self.NUMBER_SUFFIX = 'ONLY'

    def format(self, number):
        if number is None:
            return ''
        return self.format_string(str(number))

    def format_string(self, number_str):
        if not number_str or number_str.strip() == '':
            return 'ZERO ONLY'

        parts = number_str.strip().split('.')
        integer_part = parts[0].lstrip('0') if parts[0].lstrip('0') else '0'
        fractional_part = parts[1] if len(parts) > 1 else None

        if integer_part == '0' or integer_part == '':
            result = 'ZERO'
        else:
            # Pad to a multiple of three
            padded = integer_part[::-1]
            while len(padded) % 3 != 0:
                padded += '0'

            groups = []
            for i in range(0, len(padded), 3):
                groups.append(padded[i:i+3][::-1])

            result_parts = []
            for i in range(len(groups) - 1, -1, -1):
                group = groups[i]
                magnitude_index = i
                group_words = self.trans_three(group)
                if group_words:
                    chunk = self.parse_more(group_words, magnitude_index)
                    result_parts.append(chunk)

            result = ' '.join(result_parts) if result_parts else 'ZERO'

        if fractional_part is not None:
            cents = (fractional_part + '0')[:2]
            cents_words = self.trans_two(cents)
            result = result + ' AND CENTS ' + cents_words

        return result + ' ONLY'

    def parse_more(self, group_words, magnitude_index):
        if magnitude_index == 0:
            return group_words
        return group_words + ' ' + self.MAGNITUDES[magnitude_index]

    def trans_three(self, group):
        group = group.zfill(3)
        hundreds_digit = int(group[0])
        remainder = group[1:]

        result = ''
        if hundreds_digit != 0:
            result = self.SINGLE_DIGITS[hundreds_digit] + ' HUNDRED AND'
            remainder_words = self.trans_two(remainder)
            if remainder_words:
                result = result + ' ' + remainder_words
        else:
            result = self.trans_two(remainder)

        return result

    def trans_two(self, two_str):
        two_str = two_str.zfill(2)
        tens_digit = int(two_str[0])
        ones_digit = int(two_str[1])

        if tens_digit == 0 and ones_digit == 0:
            return ''
        elif tens_digit == 0:
            return self.SINGLE_DIGITS[ones_digit]
        elif tens_digit == 1:
            return self.TEENS[ones_digit]
        elif ones_digit == 0:
            return self.TENS[tens_digit]
        else:
            return self.TENS[tens_digit] + ' ' + self.SINGLE_DIGITS[ones_digit]

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
