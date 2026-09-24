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
