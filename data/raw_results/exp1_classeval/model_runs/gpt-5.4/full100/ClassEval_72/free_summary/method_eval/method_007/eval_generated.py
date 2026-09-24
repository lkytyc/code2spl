import re


class RegexUtils:
    def match(self, pattern, text):
        return re.match(pattern, text) is not None

    def findall(self, pattern, text):
        return re.findall(pattern, text)

    def split(self, pattern, text):
        return re.split(pattern, text)

    def sub(self, pattern, repl, text):
        return re.sub(pattern, repl, text)

    def email_pattern(self):
        return r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

    def phone_number_pattern(self):
        return r'^\d{3}-\d{3}-\d{4}$'

    def sentence_split_pattern(self):
        return r'(?<=[.!?]) {1,2}(?=[A-Z])'

    def split_sentences(self, text):
        return self.split(self.sentence_split_pattern(), text)

    def validate_phone_number(self, phone_number):
        return self.match(self.phone_number_pattern(), phone_number)

    def extract_email(self, text):
        return self.findall(self.email_pattern(), text)

import unittest

class RegexUtilsTestSplitSentences(unittest.TestCase):
    def test_split_sentences_1(self):
        ru = RegexUtils()
        res = ru.split_sentences("Aaa. Bbbb? Ccc!")
        self.assertEqual(res, ['Aaa', 'Bbbb', 'Ccc!'])

    def test_split_sentences_2(self):
        ru = RegexUtils()
        res = ru.split_sentences("Aaa.Bbbb? Ccc!")
        self.assertEqual(res, ['Aaa.Bbbb', 'Ccc!'])

    def test_split_sentences_3(self):
        ru = RegexUtils()
        res = ru.split_sentences("Aaa. bbbb? Ccc!")
        self.assertEqual(res, ['Aaa. bbbb', 'Ccc!'])

    def test_split_sentences_4(self):
        ru = RegexUtils()
        res = ru.split_sentences("Aaa. bbbb, Ccc!")
        self.assertEqual(res, ['Aaa. bbbb, Ccc!'])

    def test_split_sentences_5(self):
        ru = RegexUtils()
        res = ru.split_sentences("Aaa, Bbbb? Ccc!")
        self.assertEqual(res, ['Aaa, Bbbb', 'Ccc!'])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
