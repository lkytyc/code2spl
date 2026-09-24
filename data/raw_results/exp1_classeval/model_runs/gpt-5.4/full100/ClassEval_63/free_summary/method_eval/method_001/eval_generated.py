class NLPDataProcessor2:
    def process_data(self, string_list):
        import re
        processed = []
        for s in string_list:
            cleaned = re.sub(r"[^a-zA-Z\s]", "", s.lower())
            processed.append(cleaned.split())
        return processed

    def calculate_word_frequency(self, words_list):
        from collections import Counter
        counter = Counter()
        for words in words_list:
            counter.update(words)
        return dict(counter.most_common(5))

    def process(self, string_list):
        words_list = self.process_data(string_list)
        return self.calculate_word_frequency(words_list)

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
