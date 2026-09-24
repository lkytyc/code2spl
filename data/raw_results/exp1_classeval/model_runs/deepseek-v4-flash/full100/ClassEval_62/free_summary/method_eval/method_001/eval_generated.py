class NLPDataProcessor:
    def create_stop_word_list(self):
        return ["a", "an", "the"]

    def get_stop_word_list(self):
        return self.create_stop_word_list()

    def remove_stop_words(self, input_list, stop_word_list):
        output = []
        for text in input_list:
            words = text.split()
            for word in words:
                if word in stop_word_list:
                    words.remove(word)
            output.append(words)
        return output

    def process(self, input_list):
        stop_words = self.get_stop_word_list()
        return self.remove_stop_words(input_list, stop_words)

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
