import re
from collections import Counter

class NLPDataProcessor2:
    def process_data(self, strings):
        result = []
        for text in strings:
            cleaned = re.sub(r'[^a-z\s]', '', text.lower())
            result.append(cleaned.split())
        return result

    def calculate_word_frequency(self, word_lists):
        counter = Counter()
        for words in word_lists:
            counter.update(words)
        top_five = counter.most_common(5)
        return dict(top_five)

    def process(self, strings):
        word_lists = self.process_data(strings)
        return self.calculate_word_frequency(word_lists)

import unittest

class NLPDataProcessorTestCalculate(unittest.TestCase):

    def setUp(self):
        self.processor = NLPDataProcessor2()

    def test_calculate_word_frequency(self):
        words_list = [['hello', 'world'], ['this', 'is', 'a', 'test'], ['hello', 'world', 'this', 'is', 'another', 'test'],
                      ['hello', 'hello', 'world']]
        expected_output = {'hello': 4, 'world': 3, 'this': 2, 'is': 2, 'test': 2}
        self.assertEqual(self.processor.calculate_word_frequency(words_list), expected_output)

    def test_calculate_word_frequency2(self):
        words_list = [['hello', 'world'], ['this', 'is', 'a', 'test'], ['hello', 'world', 'this', 'is', 'another', 'test'],
                      ['hello', 'hello', 'world'], ['world', 'world', 'world']]
        expected_output = {'world': 6, 'hello': 4, 'this': 2, 'is': 2, 'test': 2}
        self.assertEqual(self.processor.calculate_word_frequency(words_list), expected_output)

    def test_calculate_word_frequency3(self):
        words_list = [['hello', 'world'], ['hello', 'hello', 'world'], ['world', 'world']]
        expected_output = {'world': 4, 'hello': 3}
        self.assertEqual(self.processor.calculate_word_frequency(words_list), expected_output)

    def test_calculate_word_frequency4(self):
        words_list = [['hello', 'world'], ['this', 'is', 'a', '%%%'], ['hello', 'world', 'this', 'is', 'another', '%%%'],
                      ['hello', 'hello', 'world'], ['%%%', 'world', 'a', '%%%'], ['%%%', 'hello', '%%%']]
        expected_output = {'%%%': 6, 'hello': 5, 'world': 4, 'is': 2, 'this': 2}
        self.assertEqual(self.processor.calculate_word_frequency(words_list), expected_output)

    def test_calculate_word_frequency5(self):
        words_list = [['hello', 'world'], ['this', 'is', 'a', '%%%'], ['hello', 'world', 'this', 'is', 'another', '%%%'],
                      ['hello', 'hello', 'world'], ['%%%', 'world', 'a', '%%%'], ['%%%', 'hello', '%%%'], ['hello', 'world'], ['this', 'is', 'a', '%%%'], ['hello', 'world', 'this', 'is', 'another', '%%%'],
                      ['hello', 'hello', 'world'], ['%%%', 'world', 'a', '%%%'], ['%%%', 'hello', '%%%']]
        expected_output = {'%%%': 12, 'hello': 10, 'world': 8, 'is': 4, 'this': 4}
        self.assertEqual(self.processor.calculate_word_frequency(words_list), expected_output)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
