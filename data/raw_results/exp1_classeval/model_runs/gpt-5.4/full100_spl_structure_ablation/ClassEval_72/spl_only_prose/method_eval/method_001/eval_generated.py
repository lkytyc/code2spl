class RegexUtils:
    def extract_email(self, text: str) -> list:
        pattern = self.generate_email_pattern()
        return self.findall(pattern, text)

    @staticmethod
    def findall(pattern, text: str) -> list:
        import re
        result = re.findall(pattern, text)
        return result

    @staticmethod
    def generate_email_pattern() -> str:
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        return pattern

    @staticmethod
    def generate_phone_number_pattern() -> str:
        pattern = r"\b\d{3}-\d{3}-\d{4}\b"
        return pattern

    @staticmethod
    def generate_split_sentences_pattern() -> str:
        pattern = r"[.!?][\s]{1,2}(?=[A-Z])"
        return pattern

    @staticmethod
    def match(pattern: str, text: str) -> bool:
        import re
        ans = re.match(pattern, text)
        if ans:
            return True
        return False

    @staticmethod
    def split(pattern, text: str) -> list:
        import re
        split_result = re.split(pattern, text)
        return split_result

    def split_sentences(self, text: str) -> list:
        pattern = self.generate_split_sentences_pattern()
        return self.split(pattern, text)

    @staticmethod
    def sub(pattern, replacement, text: str) -> str:
        import re
        substitution_result = re.sub(pattern, replacement, text)
        return substitution_result

    def validate_phone_number(self, phone_number) -> bool:
        pattern = self.generate_phone_number_pattern()
        return self.match(pattern, phone_number)

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
