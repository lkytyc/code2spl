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
