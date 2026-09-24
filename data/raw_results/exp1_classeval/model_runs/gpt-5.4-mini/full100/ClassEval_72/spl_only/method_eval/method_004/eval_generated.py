import re


class RegexUtils:
    @staticmethod
    def match(pattern, text):
        ans = re.match(pattern, text)
        if ans:
            return True
        return False

    @staticmethod
    def findall(pattern, text):
        matches = re.findall(pattern, text)
        return matches

    @staticmethod
    def split(pattern, text):
        result = re.split(pattern, text)
        return result

    @staticmethod
    def sub(pattern, replacement, text):
        result = re.sub(pattern, replacement, text)
        return result

    @staticmethod
    def generate_email_pattern():
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        return pattern

    @staticmethod
    def generate_phone_number_pattern():
        pattern = r"\b\d{3}-\d{3}-\d{4}\b"
        return pattern

    def generate_split_sentences_pattern(self):
        pattern = r'[.!?][\s]{1,2}(?=[A-Z])'
        return pattern

    def split_sentences(self, text):
        pattern = self.generate_split_sentences_pattern()
        result = re.split(pattern, text)
        return result

    def validate_phone_number(self, phone_number):
        pattern = self.generate_phone_number_pattern()
        result = self.match(pattern, phone_number)
        return result

    def extract_email(self, text):
        pattern = self.generate_email_pattern()
        result = self.findall(pattern, text)
        return result

import unittest

class RegexUtilsTestGenerateEmailPattern(unittest.TestCase):
    def test_generate_email_pattern_1(self):
        ru = RegexUtils()
        pat = ru.generate_email_pattern()
        res = ru.match(pat, 'iustd87t2euh@163.com')
        self.assertEqual(res, True)

    def test_generate_email_pattern_2(self):
        ru = RegexUtils()
        pat = ru.generate_email_pattern()
        res = ru.match(pat, 'iustd87t2euhifg.com')
        self.assertEqual(res, False)

    def test_generate_email_pattern_3(self):
        ru = RegexUtils()
        pat = ru.generate_email_pattern()
        res = ru.match(pat, 'iustd87t2euhifg@.com')
        self.assertEqual(res, False)

    def test_generate_email_pattern_4(self):
        ru = RegexUtils()
        pat = ru.generate_email_pattern()
        res = ru.match(pat, 'iustd87t2euhifg@.')
        self.assertEqual(res, False)

    def test_generate_email_pattern_5(self):
        ru = RegexUtils()
        pat = ru.generate_email_pattern()
        res = ru.match(pat, 'iustd87t2euhifg@com.')
        self.assertEqual(res, False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
