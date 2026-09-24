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
