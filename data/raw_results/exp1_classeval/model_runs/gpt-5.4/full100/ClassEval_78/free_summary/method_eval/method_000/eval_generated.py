class SplitSentence:
    def split_sentences(self, text):
        import re
        pattern = r'(?<!\b(?:Mr|Mrs|Ms|Dr|Prof|Sr|Jr|St|vs|etc|e\.g|i\.e))(?<=[.?])\s+'
        return re.split(pattern, text.strip()) if text.strip() else []

    def count_words(self, sentence):
        import re
        cleaned = re.sub(r'[^A-Za-z\s]', '', sentence)
        words = cleaned.split()
        return len(words)

    def process_text_file(self, text):
        sentences = self.split_sentences(text)
        if not sentences:
            return 0
        return max(self.count_words(sentence) for sentence in sentences)

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
