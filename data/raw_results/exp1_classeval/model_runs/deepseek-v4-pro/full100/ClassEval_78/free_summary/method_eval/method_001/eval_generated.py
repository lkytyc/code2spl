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

class SplitSentenceTestCountWords(unittest.TestCase):
    def test_count_words_1(self):
        ss = SplitSentence()
        cnt = ss.count_words("abc def")
        self.assertEqual(cnt, 2)

    def test_count_words_2(self):
        ss = SplitSentence()
        cnt = ss.count_words("abc def 1")
        self.assertEqual(cnt, 2)

    def test_count_words_3(self):
        ss = SplitSentence()
        cnt = ss.count_words("abc 1")
        self.assertEqual(cnt, 1)

    def test_count_words_4(self):
        ss = SplitSentence()
        cnt = ss.count_words("abc def bbb1")
        self.assertEqual(cnt, 3)

    def test_count_words_5(self):
        ss = SplitSentence()
        cnt = ss.count_words("abc def 111")
        self.assertEqual(cnt, 2)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
