import re

class RegexUtils:
    @staticmethod
    def match(pattern, text):
        return re.match(pattern, text) is not None

    @staticmethod
    def findall(pattern, text):
        return re.findall(pattern, text)

    @staticmethod
    def split(pattern, text):
        return re.split(pattern, text)

    @staticmethod
    def sub(pattern, replacement, text):
        return re.sub(pattern, replacement, text)

    @staticmethod
    def generate_email_pattern():
        return r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

    @staticmethod
    def generate_phone_number_pattern():
        return r'\d{3}-\d{3}-\d{4}'

    @staticmethod
    def generate_split_sentences_pattern():
        return r'(?<=[.!?])\s{1,2}(?=[A-Z])'

    @classmethod
    def split_sentences(cls, text):
        return cls.split(cls.generate_split_sentences_pattern(), text)

    @classmethod
    def validate_phone_number(cls, phone_number):
        return cls.match(r'^' + cls.generate_phone_number_pattern() + r'$', phone_number)

    @classmethod
    def extract_email(cls, text):
        return cls.findall(cls.generate_email_pattern(), text)

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
