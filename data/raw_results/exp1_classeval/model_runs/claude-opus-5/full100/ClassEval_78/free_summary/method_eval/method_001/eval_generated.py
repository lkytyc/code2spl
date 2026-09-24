import re


class SplitSentence:

    def split_sentences(self, sentences_string):
        # Split after period or question mark followed by whitespace,
        # using two negative lookbehinds to avoid splitting on abbreviations
        # like "e.g." or "Dr."
        pattern = r'(?<!\b\w)(?<!\b\w\w)[.?]\s+'
        sentences = re.split(pattern, sentences_string)
        return [s.strip() for s in sentences if s.strip()]

    def count_words(self, sentence):
        # Strip all non-alphabetic characters, then split on whitespace
        cleaned = re.sub(r'[^a-zA-Z\s]', '', sentence)
        words = cleaned.split()
        return len(words)

    def process_text_file(self, sentences_string):
        sentences = self.split_sentences(sentences_string)
        max_word_count = 0
        for sentence in sentences:
            count = self.count_words(sentence)
            if count > max_word_count:
                max_word_count = count
        return max_word_count

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
