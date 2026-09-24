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
