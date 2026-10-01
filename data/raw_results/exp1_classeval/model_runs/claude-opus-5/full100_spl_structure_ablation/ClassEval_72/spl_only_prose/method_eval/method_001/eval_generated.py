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

class RegexUtilsTestFindall(unittest.TestCase):
    def test_findall_1(self):
        ru = RegexUtils()
        res = ru.findall(r'\b\d{3}-\d{3}-\d{4}\b', "123-456-7890 abiguygusu 876-286-9876 kjgufwycs 987-762-9767")
        self.assertEqual(res, ['123-456-7890', '876-286-9876', '987-762-9767'])

    def test_findall_2(self):
        ru = RegexUtils()
        res = ru.findall(r'\b\d{3}-\d{3}-\d{4}\b', "abiguygusu  kjgufwycs 987-762-9767")
        self.assertEqual(res, ['987-762-9767'])

    def test_findall_3(self):
        ru = RegexUtils()
        res = ru.findall(r'\b\d{3}-\d{3}-\d{4}\b', "abiguygusu  kjgufwycs ")
        self.assertEqual(res, [])

    def test_findall_4(self):
        ru = RegexUtils()
        res = ru.findall(r'\b\d{3}-\d{3}-\d{4}\b', "abiguygusu  111-111-1111 kjgufwycs 987-762-9767")
        self.assertEqual(res, ['111-111-1111', '987-762-9767'])

    def test_findall_5(self):
        ru = RegexUtils()
        res = ru.findall(r'\b\d{3}-\d{3}-\d{4}\b', "abiguygusu  111-111-111a kjgufwycs 987-762-9767")
        self.assertEqual(res, ['987-762-9767'])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
