class NLPDataProcessor:
    def construct_stop_word_list(self):
        return ['a', 'an', 'the']

    def remove_stop_words(self, string_list, stop_word_list):
        stop_words = {word.lower() for word in stop_word_list}
        result = []
        for string in string_list:
            filtered_words = []
            for word in string.split():
                if word.lower() not in stop_words:
                    filtered_words.append(word)
            result.append(filtered_words)
        return result

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
