import re

class RegexUtils:
    def match(self, pattern, text):
        return bool(re.match(pattern, text))

    def findall(self, pattern, text):
        return re.findall(pattern, text)

    def split(self, pattern, text):
        return re.split(pattern, text)

    def sub(self, pattern, replacement, text):
        return re.sub(pattern, replacement, text)

    def generate_email_pattern(self):
        return r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    def generate_phone_number_pattern(self):
        return r'\b\d{3}-\d{3}-\d{4}\b'

    def generate_split_sentences_pattern(self):
        return r'[.!?][\s]{1,2}(?=[A-Z])'

    def split_sentences(self, text):
        return self.split(self.generate_split_sentences_pattern(), text)

    def validate_phone_number(self, phone_number):
        return self.match(self.generate_phone_number_pattern(), phone_number)

    def extract_email(self, text):
        return self.findall(self.generate_email_pattern(), text)

import unittest

class RegexUtilsTestValidatePhoneNumber(unittest.TestCase):
    def test_validate_phone_number_1(self):
        ru = RegexUtils()
        res = ru.validate_phone_number("123-456-7890")
        self.assertEqual(res, True)

    def test_validate_phone_number_2(self):
        ru = RegexUtils()
        res = ru.validate_phone_number("1234567890")
        self.assertEqual(res, False)

    def test_validate_phone_number_3(self):
        ru = RegexUtils()
        res = ru.validate_phone_number("a23-456-7890")
        self.assertEqual(res, False)

    def test_validate_phone_number_4(self):
        ru = RegexUtils()
        res = ru.validate_phone_number("123-456-789")
        self.assertEqual(res, False)

    def test_validate_phone_number_5(self):
        ru = RegexUtils()
        res = ru.validate_phone_number("1234-56-789")
        self.assertEqual(res, False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
