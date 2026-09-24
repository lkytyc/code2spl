import re


class RegexUtils:

    def match(self, pattern, text):
        ans = re.match(pattern, text)
        return bool(ans)

    def findall(self, pattern, text):
        matches = re.findall(pattern, text)
        return matches

    def split(self, pattern, text):
        result = re.split(pattern, text)
        return result

    def sub(self, pattern, replacement, text):
        return re.sub(pattern, replacement, text)

    def generate_email_pattern(self):
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return pattern

    def generate_phone_number_pattern(self):
        pattern = r'\b\d{3}-\d{3}-\d{4}\b'
        return pattern

    def generate_split_sentences_pattern(self):
        pattern = '[.!?][\s]{1,2}(?=[A-Z])'
        return pattern

    def split_sentences(self, text):
        pattern = self.generate_split_sentences_pattern()
        sentences = self.split(pattern, text)
        return sentences

    def validate_phone_number(self, phone_number):
        pattern = self.generate_phone_number_pattern()
        match_result = self.match(pattern, phone_number)
        return match_result

    def extract_email(self, text):
        pattern = self.generate_email_pattern()
        return self.findall(pattern, text)

import unittest

class RegexUtilsTestSplit(unittest.TestCase):
    def test_split_1(self):
        ru = RegexUtils()
        res = ru.split(r'\b\d{3}-\d{3}-\d{4}\b', "123-456-7890 abiguygusu 876-286-9876 kjgufwycs 987-762-9767")
        self.assertEqual(res, ['', ' abiguygusu ', ' kjgufwycs ', ''])

    def test_split_2(self):
        ru = RegexUtils()
        res = ru.split(r'\b\d{3}-\d{3}-\d{4}\b', "1234567890 abiguygusu 8762869876 kjgufwycs 9877629767")
        self.assertEqual(res, ['1234567890 abiguygusu 8762869876 kjgufwycs 9877629767'])

    def test_split_3(self):
        ru = RegexUtils()
        res = ru.split(r'\b\d{3}-\d{3}-\d{4}\b', "111-111-1111 abiguygusu 876-286-9876 kjgufwycs 987-762-9767")
        self.assertEqual(res, ['', ' abiguygusu ', ' kjgufwycs ', ''])

    def test_split_4(self):
        ru = RegexUtils()
        res = ru.split(r'\b\d{3}-\d{3}-\d{4}\b', "123456-7890 abiguygusu 876-286-9876 kjgufwycs 987-762-9767")
        self.assertEqual(res, ['123456-7890 abiguygusu ', ' kjgufwycs ', ''])

    def test_split_5(self):
        ru = RegexUtils()
        res = ru.split(r'\b\d{3}-\d{3}-\d{4}\b', "123-456-789a abiguygusu 876-286-9876 kjgufwycs 987-762-9767")
        self.assertEqual(res, ['123-456-789a abiguygusu ', ' kjgufwycs ', ''])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
