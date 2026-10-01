import re


class RegexUtils:

    def extract_email(self, text: str) -> list:
        pattern = self.generate_email_pattern()
        return self.findall(pattern, text)

    def findall(self, pattern: str, text: str) -> list:
        return re.findall(pattern, text)

    def generate_email_pattern(self) -> str:
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return pattern

    def generate_phone_number_pattern(self) -> str:
        pattern = r'\b\d{3}-\d{3}-\d{4}\b'
        return pattern

    def generate_split_sentences_pattern(self) -> str:
        pattern = '[.!?][\s]{1,2}(?=[A-Z])'
        return pattern

    def match(self, pattern: str, text: str) -> bool:
        ans = re.match(pattern, text)
        if ans:
            return True
        return False

    def split(self, pattern: str, text: str) -> list:
        return re.split(pattern, text)

    def split_sentences(self, text: str) -> list:
        pattern = self.generate_split_sentences_pattern()
        sentences = self.split(pattern, text)
        return sentences

    def sub(self, pattern, replacement, text: str) -> str:
        substituted_string = re.sub(pattern, replacement, text)
        return substituted_string

    def validate_phone_number(self, phone_number: str):
        pattern = self.generate_phone_number_pattern()
        match_result = self.match(pattern, phone_number)
        return match_result

import unittest

class RegexUtilsTestGenerateSplitSentencesPattern(unittest.TestCase):
    def test_generate_split_sentences_pattern_1(self):
        ru = RegexUtils()
        pat = ru.generate_split_sentences_pattern()
        res = ru.match(pat, '? Y')
        self.assertEqual(res, True)

    def test_generate_split_sentences_pattern_2(self):
        ru = RegexUtils()
        pat = ru.generate_split_sentences_pattern()
        res = ru.match(pat, '! Y')
        self.assertEqual(res, True)

    def test_generate_split_sentences_pattern_3(self):
        ru = RegexUtils()
        pat = ru.generate_split_sentences_pattern()
        res = ru.match(pat, '? ')
        self.assertEqual(res, False)

    def test_generate_split_sentences_pattern_4(self):
        ru = RegexUtils()
        pat = ru.generate_split_sentences_pattern()
        res = ru.match(pat, '?Y')
        self.assertEqual(res, False)

    def test_generate_split_sentences_pattern_5(self):
        ru = RegexUtils()
        pat = ru.generate_split_sentences_pattern()
        res = ru.match(pat, '.Y')
        self.assertEqual(res, False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
