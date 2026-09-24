import re

class RegexUtils:
    def extract_email(self, text: str) -> list:
        pattern = self.generate_email_pattern()
        return self.findall(pattern, text)

    def findall(self, pattern, text) -> list:
        result = re.findall(pattern, text)
        return result

    def generate_email_pattern(self) -> str:
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return pattern

    def generate_phone_number_pattern(self) -> str:
        pattern = r'\b\d{3}-\d{3}-\d{4}\b'
        return pattern

    def generate_split_sentences_pattern(self) -> str:
        pattern = r'[.!?][\s]{1,2}(?=[A-Z])'
        return pattern

    def match(self, pattern: str, text: str) -> bool:
        ans = re.match(pattern, text)
        if ans:
            return True
        return False

    def split(self, pattern: str, text: str) -> list:
        split_result = re.split(pattern, text)
        return split_result

    def split_sentences(self, text: str):
        pattern = self.generate_split_sentences_pattern()
        split_result = self.split(pattern, text)
        return split_result

    def sub(self, pattern: str, replacement, text):
        result = re.sub(pattern, replacement, text)
        return result

    def validate_phone_number(self, phone_number: str):
        pattern = self.generate_phone_number_pattern()
        return self.match(pattern, phone_number)

import unittest

class RegexUtilsTestExtractEmail(unittest.TestCase):
    def test_extract_email_1(self):
        ru = RegexUtils()
        res = ru.extract_email("abcdefg@163.com ygusyfysy@126.com wljduyuv@qq.com")
        self.assertEqual(res, ['abcdefg@163.com', 'ygusyfysy@126.com', 'wljduyuv@qq.com'])

    def test_extract_email_2(self):
        ru = RegexUtils()
        res = ru.extract_email("abcdefg@.com ygusyfysy@126.com wljduyuv@qq.com")
        self.assertEqual(res, ['ygusyfysy@126.com', 'wljduyuv@qq.com'])

    def test_extract_email_3(self):
        ru = RegexUtils()
        res = ru.extract_email("abcdefgiscom ygusyfysy@126.com wljduyuv@qq.com")
        self.assertEqual(res, ['ygusyfysy@126.com', 'wljduyuv@qq.com'])

    def test_extract_email_4(self):
        ru = RegexUtils()
        res = ru.extract_email("abcdefgiscom ygusyfysy126.com wljduyuv@qq.com")
        self.assertEqual(res, ['wljduyuv@qq.com'])

    def test_extract_email_5(self):
        ru = RegexUtils()
        res = ru.extract_email("abcdefgiscom ygusyfysy@.com wljduyuv@qq.com")
        self.assertEqual(res, ['wljduyuv@qq.com'])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
