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

class RegexUtilsTestSub(unittest.TestCase):
    def test_sub_1(self):
        ru = RegexUtils()
        res = ru.sub(r'\b\d{3}-\d{3}-\d{4}\b', 'phone num',
                     "123-456-7890 abiguygusu 876-286-9876 kjgufwycs 987-762-9767")
        self.assertEqual(res, 'phone num abiguygusu phone num kjgufwycs phone num')

    def test_sub_2(self):
        ru = RegexUtils()
        res = ru.sub(r'\b\d{3}-\d{3}-\d{4}\b', 'phone num',
                     "1234567890 abiguygusu 8762869876 kjgufwycs 9877629767")
        self.assertEqual(res, "1234567890 abiguygusu 8762869876 kjgufwycs 9877629767")

    def test_sub_3(self):
        ru = RegexUtils()
        res = ru.sub(r'\b\d{3}-\d{3}-\d{4}\b', 'phone num',
                     "123456-7890 abiguygusu 876-286-9876 kjgufwycs 987-762-9767")
        self.assertEqual(res, '123456-7890 abiguygusu phone num kjgufwycs phone num')

    def test_sub_4(self):
        ru = RegexUtils()
        res = ru.sub(r'\b\d{3}-\d{3}-\d{4}\b', 'phone num',
                     "123-456-789a abiguygusu 876-286-9876 kjgufwycs 987-762-9767")
        self.assertEqual(res, '123-456-789a abiguygusu phone num kjgufwycs phone num')

    def test_sub_5(self):
        ru = RegexUtils()
        res = ru.sub(r'\b\d{3}-\d{3}-\d{4}\b', 'phone num',
                     "123-456-780 abiguygusu 876-286-9876 kjgufwycs 987-762-9767")
        self.assertEqual(res, '123-456-780 abiguygusu phone num kjgufwycs phone num')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
