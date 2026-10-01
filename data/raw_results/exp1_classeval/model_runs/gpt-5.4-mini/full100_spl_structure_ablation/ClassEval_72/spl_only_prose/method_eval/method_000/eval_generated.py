import re


class RegexUtils:
    def extract_email(self, text: str):
        pattern = self.generate_email_pattern()
        return self.findall(pattern, text)

    def findall(self, pattern: str, text: str):
        matches = re.findall(pattern, text)
        return matches

    @staticmethod
    def generate_email_pattern() -> str:
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        return pattern

    @staticmethod
    def generate_phone_number_pattern() -> str:
        pattern = r"\b\d{3}-\d{3}-\d{4}\b"
        return pattern

    def generate_split_sentences_pattern(self) -> str:
        pattern = r'[.!?][\s]{1,2}(?=[A-Z])'
        return pattern

    @staticmethod
    def match(pattern, text: str) -> bool:
        ans = re.match(pattern, text)
        if ans:
            return True
        if not ans:
            return False

    def split(self, pattern: str, text: str):
        result = re.split(pattern, text)
        return result

    @staticmethod
    def split_sentences(text: str):
        pattern = RegexUtils.generate_split_sentences_pattern()
        result = re.split(pattern, text)
        return result

    def sub(self, pattern, replacement, text: str):
        result = re.sub(pattern, replacement, text)
        return result

    def validate_phone_number(self, phone_number):
        pattern = self.generate_phone_number_pattern()
        result = self.match(pattern, phone_number)
        return result

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
