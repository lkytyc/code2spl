import re
from collections import Counter
from typing import Iterable

class NLPDataProcessor2:
    def process_data(self, string_list: list[str]) -> list[list[str]]:
        words_list = []
        for string in string_list:
            processed_string = string.lower()
            processed_string = re.sub(r'[^a-zA-Z\s]', '', processed_string)
            words = processed_string.split()
            words_list.append(words)
        return words_list

    def calculate_word_frequency(self, words_list: list[Iterable[str]]) -> dict[str, int]:
        word_frequency = Counter()
        for words in words_list:
            word_frequency.update(words)
        sorted_word_frequency = dict(sorted(word_frequency.items(), key=lambda item: item[1], reverse=True))
        top_5_word_frequency = dict(list(sorted_word_frequency.items())[:5])
        return top_5_word_frequency

    def process(self, string_list: list) -> dict:
        words_list = self.process_data(string_list)
        word_frequency_dict = self.calculate_word_frequency(words_list)
        return word_frequency_dict

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
