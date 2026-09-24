import re


class RegexUtils:
    def match(self, pattern: str, text: str) -> bool:
        ans = re.match(pattern, text)
        if ans:
            return True
        return False

    def findall(self, pattern, text):
        result = re.findall(pattern, text)
        return result

    def split(self, pattern: str, text: str):
        split_result = re.split(pattern, text)
        return split_result

    def sub(self, pattern: str, replacement, text):
        result = re.sub(pattern, replacement, text)
        return result

    def generate_email_pattern(self) -> str:
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return pattern

    def generate_phone_number_pattern(self) -> str:
        pattern = r"\b\d{3}-\d{3}-\d{4}\b"
        return pattern

    def generate_split_sentences_pattern(self) -> str:
        pattern = r"[.!?][\s]{1,2}(?=[A-Z])"
        return pattern

    def split_sentences(self, text: str):
        pattern = self.generate_split_sentences_pattern()
        split_result = self.split(pattern, text)
        return split_result

    def validate_phone_number(self, phone_number: str):
        pattern = self.generate_phone_number_pattern()
        return_value = self.match(pattern, phone_number)
        return return_value

    def extract_email(self, text: str):
        pattern = self.generate_email_pattern()
        return_value = self.findall(pattern, text)
        return return_value

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
