class SplitSentence:
    def count_words(self, sentence: str) -> int:
        import re

        sentence = re.sub(r"[^a-zA-Z\s]", "", sentence)
        words = sentence.split()
        return len(words)

    def process_text_file(self, sentences_string: str) -> int:
        sentences = self.split_sentences(sentences_string)
        max_count = 0

        for sentence in sentences:
            count = self.count_words(sentence)
            if count > max_count:
                max_count = count

        return max_count

    def split_sentences(self, sentences_string: str) -> list[str]:
        import re

        pattern = (
            r"(?<!Mr\.)(?<!Mrs\.)(?<!Ms\.)(?<!Dr\.)(?<!Prof\.)"
            r"(?<!Sr\.)(?<!Jr\.)(?<!e\.g\.)(?<!i\.e\.)(?<=[.?])\s+"
        )
        sentences = re.split(pattern, sentences_string)
        return sentences

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
