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

class RegexUtilsTestSplitSentences(unittest.TestCase):
    def test_split_sentences_1(self):
        ru = RegexUtils()
        res = ru.split_sentences("Aaa. Bbbb? Ccc!")
        self.assertEqual(res, ['Aaa', 'Bbbb', 'Ccc!'])

    def test_split_sentences_2(self):
        ru = RegexUtils()
        res = ru.split_sentences("Aaa.Bbbb? Ccc!")
        self.assertEqual(res, ['Aaa.Bbbb', 'Ccc!'])

    def test_split_sentences_3(self):
        ru = RegexUtils()
        res = ru.split_sentences("Aaa. bbbb? Ccc!")
        self.assertEqual(res, ['Aaa. bbbb', 'Ccc!'])

    def test_split_sentences_4(self):
        ru = RegexUtils()
        res = ru.split_sentences("Aaa. bbbb, Ccc!")
        self.assertEqual(res, ['Aaa. bbbb, Ccc!'])

    def test_split_sentences_5(self):
        ru = RegexUtils()
        res = ru.split_sentences("Aaa, Bbbb? Ccc!")
        self.assertEqual(res, ['Aaa, Bbbb', 'Ccc!'])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
