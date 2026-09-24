import re

class RegexUtils:
    """
    The class provides to match, find all occurrences, split, and substitute text using regular expressions. It also includes predefined patterns, validating phone numbers and extracting email addresses.
    """

    def match(self, pattern, text):
        ans = re.match(pattern, text)
        if ans:
            return True
        else:
            return False

    def findall(self, pattern, text):
        result = re.findall(pattern, text)
        return result

    def split(self, pattern, text):
        split_result = re.split(pattern, text)
        return split_result

    def sub(self, pattern, replacement, text):
        result = re.sub(pattern, replacement, text)
        return result

    def generate_email_pattern(self):
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return pattern

    def generate_phone_number_pattern(self):
        pattern = r'\b\d{3}-\d{3}-\d{4}\b'
        return pattern

    def generate_split_sentences_pattern(self):
        pattern = r'[.!?][\s]{1,2}(?=[A-Z])'
        return pattern

    def split_sentences(self, text):
        pattern = self.generate_split_sentences_pattern()
        split_result = self.split(pattern, text)
        return split_result

    def validate_phone_number(self, phone_number):
        pattern = self.generate_phone_number_pattern()
        return_value = self.match(pattern, phone_number)
        return return_value

    def extract_email(self, text):
        pattern = self.generate_email_pattern()
        return_value = self.findall(pattern, text)
        return return_value

import unittest

class RegexUtilsTestGeneratePhoneNumberPattern(unittest.TestCase):
    def test_generate_phone_number_pattern_1(self):
        ru = RegexUtils()
        pat = ru.generate_phone_number_pattern()
        res = ru.match(pat, '123-456-7890')
        self.assertEqual(res, True)

    def test_generate_phone_number_pattern_2(self):
        ru = RegexUtils()
        pat = ru.generate_phone_number_pattern()
        res = ru.match(pat, '1234567890')
        self.assertEqual(res, False)

    def test_generate_phone_number_pattern_3(self):
        ru = RegexUtils()
        pat = ru.generate_phone_number_pattern()
        res = ru.match(pat, '123-456-789')
        self.assertEqual(res, False)

    def test_generate_phone_number_pattern_4(self):
        ru = RegexUtils()
        pat = ru.generate_phone_number_pattern()
        res = ru.match(pat, 'a23-456-7890')
        self.assertEqual(res, False)

    def test_generate_phone_number_pattern_5(self):
        ru = RegexUtils()
        pat = ru.generate_phone_number_pattern()
        res = ru.match(pat, '1234-56-7890')
        self.assertEqual(res, False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
