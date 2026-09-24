import re

class RegexUtils:
    EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    PHONE_PATTERN = r"(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}"
    SENTENCE_PATTERN = r"(?<=[.!?])\s+"

    def match(self, pattern, text):
        return re.match(pattern, text)

    def findall(self, pattern, text):
        return re.findall(pattern, text)

    def find_all(self, pattern, text):
        return self.findall(pattern, text)

    def split(self, pattern, text):
        return re.split(pattern, text)

    def sub(self, pattern, replacement, text):
        return re.sub(pattern, replacement, text)

    def substitute(self, pattern, replacement, text):
        return self.sub(pattern, replacement, text)

    def validate_phone_number(self, phone_number):
        return bool(re.fullmatch(self.PHONE_PATTERN, phone_number.strip()))

    def extract_email_addresses(self, text):
        return re.findall(self.EMAIL_PATTERN, text)

    def split_sentences(self, text):
        return [sentence.strip() for sentence in re.split(self.SENTENCE_PATTERN, text.strip()) if sentence.strip()]

    validate_phone = validate_phone_number
    extract_emails = extract_email_addresses

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
