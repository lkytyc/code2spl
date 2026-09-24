class NLPDataProcessor:
    def construct_stop_word_list(self):
        return ["a", "an", "the"]

    def remove_stop_words(self, string_list, stop_word_list):
        processed_list = []
        for string_item in string_list:
            words = string_item.split()
            for word in words:
                if word in stop_word_list:
                    words.remove(word)
            processed_list.append(words)
        return processed_list

    def process(self, string_list):
        stop_word_list = self.construct_stop_word_list()
        return self.remove_stop_words(string_list, stop_word_list)

import unittest

class NLPDataProcessorTestConstruct(unittest.TestCase):
    def setUp(self):
        self.processor = NLPDataProcessor()

    def test_construct_stop_word_list(self):
        stop_word_list = self.processor.construct_stop_word_list()
        expected_stop_words = ['a', 'an', 'the']
        self.assertEqual(stop_word_list, expected_stop_words)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
