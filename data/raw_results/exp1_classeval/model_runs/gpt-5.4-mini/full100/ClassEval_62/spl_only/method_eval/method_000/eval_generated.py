class NLPDataProcessor:
    def construct_stop_word_list(self):
        stop_word_list = ['a', 'an', 'the']
        return stop_word_list

    def remove_stop_words(self, string_list, stop_word_list):
        answer = []
        for string in string_list:
            string_split = string.split()
            for word in string_split[:]:
                if word in stop_word_list:
                    string_split.remove(word)
            answer.append(string_split)
        return answer

    def process(self, string_list):
        stop_word_list = self.construct_stop_word_list()
        words_list = self.remove_stop_words(string_list, stop_word_list)
        return words_list

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
