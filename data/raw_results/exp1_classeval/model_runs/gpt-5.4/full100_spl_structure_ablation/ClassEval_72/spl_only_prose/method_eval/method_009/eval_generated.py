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
