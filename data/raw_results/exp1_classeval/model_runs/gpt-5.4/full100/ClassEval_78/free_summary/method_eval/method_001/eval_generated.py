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
