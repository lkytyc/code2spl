class NLPDataProcessor:

    def construct_stop_word_list(self):
        return ['a', 'an', 'the']

    def remove_stop_words(self, string_list, stop_word_list):
        accumulator = []
        for string in string_list:
            tokens = string.split()
            for token in tokens:
                if token in stop_word_list:
                    tokens.remove(token)
            accumulator.append(tokens)
        return accumulator

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
