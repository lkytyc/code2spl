import re

class SplitSentence:
    def split_sentences(self, text):
        pattern = r'(?<!e\.g\.)(?<!\b[A-Z]\.)(?<=[.!?])\s+'
        return re.split(pattern, text)

    def count_words(self, sentence):
        cleaned = re.sub(r'[^A-Za-z\s]', '', sentence)
        words = cleaned.split()
        return len(words)

    def process_text_file(self, full_text):
        sentences = self.split_sentences(full_text)
        max_words = 0
        for sentence in sentences:
            word_count = self.count_words(sentence)
            if word_count > max_words:
                max_words = word_count
        return max_words

import unittest

class SplitSentenceTestProcessTextFile(unittest.TestCase):
    def test_process_text_file_1(self):
        ss = SplitSentence()
        cnt = ss.process_text_file("aaa aaaa. bb bbbb bbb? cccc ccccccc cc ccc. dd ddd?")
        self.assertEqual(cnt, 4)

    def test_process_text_file_2(self):
        ss = SplitSentence()
        cnt = ss.process_text_file("Mr. Smith is a teacher. Yes.")
        self.assertEqual(cnt, 5)

    def test_process_text_file_3(self):
        ss = SplitSentence()
        cnt = ss.process_text_file("Mr. Smith is a teacher. Yes 1 2 3 4 5 6.")
        self.assertEqual(cnt, 5)

    def test_process_text_file_4(self):
        ss = SplitSentence()
        cnt = ss.process_text_file("aaa aaaa. bb bbbb bbb? cccc ccccccc cc ccc.")
        self.assertEqual(cnt, 4)

    def test_process_text_file_5(self):
        ss = SplitSentence()
        cnt = ss.process_text_file("aaa aaaa. bb bbbb bbb?")
        self.assertEqual(cnt, 3)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
