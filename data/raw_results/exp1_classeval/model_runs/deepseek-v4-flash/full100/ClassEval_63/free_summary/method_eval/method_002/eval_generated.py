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

class NLPDataProcessorTestProcess(unittest.TestCase):

    def setUp(self):
        self.processor = NLPDataProcessor2()

    def test_process(self):
        string_list = ["Hello World!", "This is a test.", "Hello World, this is a test."]
        expected_output = {'hello': 2, 'world': 2, 'this': 2, 'is': 2, 'a': 2}
        self.assertEqual(self.processor.process(string_list), expected_output)

    def test_process2(self):
        string_list = []
        expected_output = []
        self.assertEqual(self.processor.process_data(string_list), expected_output)

    def test_calculate3(self):
        words_list = []
        expected_output = {}
        self.assertEqual(self.processor.calculate_word_frequency(words_list), expected_output)

    def test_process4(self):
        string_list = ["@#$%^&*", "Special_Characters", "12345"]
        expected_output = [[], ['specialcharacters'], []]
        self.assertEqual(self.processor.process_data(string_list), expected_output)

    def test_process5(self):
        string_list = ["Hello World! %%%", "This is a %%% test. %%% ", "Hello World, this is a test. %%%"]
        expected_output = {'hello': 2, 'world': 2, 'this': 2, 'is': 2, 'a': 2}
        self.assertEqual(self.processor.process(string_list), expected_output)

    def test_process6(self):
        string_list = ["12345", "67890", "98765"]
        expected_output = [[], [], []]
        self.assertEqual(self.processor.process_data(string_list), expected_output)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
