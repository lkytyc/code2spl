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

class SplitSentenceTestSplitSentences(unittest.TestCase):
    def test_split_sentences_1(self):
        ss = SplitSentence()
        lst = ss.split_sentences("aaa aaaa. bb bbbb bbb? cccc cccc. dd ddd?")
        self.assertEqual(lst, ['aaa aaaa.', 'bb bbbb bbb?', 'cccc cccc.', 'dd ddd?'])

    def test_split_sentences_2(self):
        ss = SplitSentence()
        lst = ss.split_sentences("Who is Mr. Smith? He is a teacher.")
        self.assertEqual(lst, ['Who is Mr. Smith?', 'He is a teacher.'])

    def test_split_sentences_3(self):
        ss = SplitSentence()
        lst = ss.split_sentences("Who is A.B.C.? He is a teacher.")
        self.assertEqual(lst, ['Who is A.B.C.?', 'He is a teacher.'])

    def test_split_sentences_4(self):
        ss = SplitSentence()
        lst = ss.split_sentences("aaa aaaa. bb bbbb bbb? cccc cccc.")
        self.assertEqual(lst, ['aaa aaaa.', 'bb bbbb bbb?', 'cccc cccc.'])

    def test_split_sentences_5(self):
        ss = SplitSentence()
        lst = ss.split_sentences("aaa aaaa. bb bbbb bbb?")
        self.assertEqual(lst, ['aaa aaaa.', 'bb bbbb bbb?'])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
