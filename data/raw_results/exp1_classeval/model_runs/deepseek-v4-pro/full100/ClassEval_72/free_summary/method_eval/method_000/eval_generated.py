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
        return r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    @staticmethod
    def generate_phone_number_pattern():
        return r'\b\d{3}-\d{3}-\d{4}\b'

    @staticmethod
    def generate_split_sentences_pattern():
        return r'(?<=[.!?])\s+(?=[A-Z])'

    @classmethod
    def split_sentences(cls, text):
        pattern = cls.generate_split_sentences_pattern()
        return cls.split(pattern, text)

    @classmethod
    def validate_phone_number(cls, phone_number):
        pattern = cls.generate_phone_number_pattern()
        return cls.match(pattern, phone_number)

    @classmethod
    def extract_email(cls, text):
        pattern = cls.generate_email_pattern()
        return cls.findall(pattern, text)

import unittest

class RegexUtilsTestMatch(unittest.TestCase):
    def test_match_1(self):
        ru = RegexUtils()
        res = ru.match(r'\b\d{3}-\d{3}-\d{4}\b', "123-456-7890")
        self.assertEqual(res, True)

    def test_match_2(self):
        ru = RegexUtils()
        res = ru.match(r'\b\d{3}-\d{3}-\d{4}\b', "1234567890")
        self.assertEqual(res, False)

    def test_match_3(self):
        ru = RegexUtils()
        res = ru.match(r'\b\d{3}-\d{3}-\d{4}\b', "111-111-1111")
        self.assertEqual(res, True)

    def test_match_4(self):
        ru = RegexUtils()
        res = ru.match(r'\b\d{3}-\d{3}-\d{4}\b', "123-456-789")
        self.assertEqual(res, False)

    def test_match_5(self):
        ru = RegexUtils()
        res = ru.match(r'\b\d{3}-\d{3}-\d{4}\b', "123-456-789a")
        self.assertEqual(res, False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
