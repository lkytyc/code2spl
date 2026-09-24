class NLPDataProcessor:
    def construct_stop_word_list(self):
        return ['a', 'an', 'the']

    def remove_stop_words(self, texts, stop_words):
        output = []
        for text in texts:
            words = text.split()
            filtered = [word for word in words if word not in stop_words]
            output.append(filtered)
        return output

    def process(self, texts):
        stop_words = self.construct_stop_word_list()
        return self.remove_stop_words(texts, stop_words)

import unittest

class NLPDataProcessorTestRemove(unittest.TestCase):
    def setUp(self):
        self.processor = NLPDataProcessor()

    def test_remove_stop_words(self):
        string_list = ['This is a test', 'This is an apple', 'This is the dog']
        stop_word_list = ['a', 'an', 'the']
        words_list = self.processor.remove_stop_words(string_list, stop_word_list)
        expected_words_list = [['This', 'is', 'test'], ['This', 'is', 'apple'], ['This', 'is', 'dog']]
        self.assertEqual(words_list, expected_words_list)

    def test_remove_stop_words_2(self):
        string_list = ['a', 'an', 'the']
        stop_word_list = ['a', 'an', 'the']
        words_list = self.processor.remove_stop_words(string_list, stop_word_list)
        self.assertEqual(words_list, [[], [], []])

    def test_remove_stop_words_3(self):
        string_list = []
        stop_word_list = ['a', 'an', 'the']
        words_list = self.processor.remove_stop_words(string_list, stop_word_list)
        self.assertEqual(words_list, [])

    def test_remove_stop_words_4(self):
        string_list = ['This is a test', 'This is an apple', 'This is the dog']
        stop_word_list = []
        words_list = self.processor.remove_stop_words(string_list, stop_word_list)
        expected_words_list = [['This', 'is', 'a', 'test'], ['This', 'is', 'an', 'apple'], ['This', 'is', 'the', 'dog']]
        self.assertEqual(words_list, expected_words_list)

    def test_remove_stop_words_5(self):
        string_list = ['This is a test', 'This is an apple', 'This is the dog']
        stop_word_list = ['a', 'an', 'the', 'This', 'is']
        words_list = self.processor.remove_stop_words(string_list, stop_word_list)
        expected_words_list = [['is', 'test'], ['is', 'apple'], ['is', 'dog']]
        self.assertEqual(words_list, expected_words_list)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
