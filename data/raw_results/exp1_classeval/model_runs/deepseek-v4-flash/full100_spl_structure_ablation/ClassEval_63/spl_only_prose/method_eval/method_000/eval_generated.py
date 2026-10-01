from collections import Counter
from typing import Iterable, Dict, List

class NLPDataProcessor2:
    def calculate_word_frequency(self, words_list: Iterable[Iterable[str]]) -> Dict[str, int]:
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

    def process_data(self, string_list: List[str]) -> List[List[str]]:
        import re
        words_list = []
        for string in string_list:
            processed_string = string.lower()
            processed_string = re.sub(r'[^a-zA-Z\s]', '', processed_string)
            words = processed_string.split()
            words_list.append(words)
        return words_list

import unittest

class NLPDataProcessorTestProcessData(unittest.TestCase):

    def setUp(self):
        self.processor = NLPDataProcessor2()

    def test_process_data(self):
        string_list = ["Hello World!", "This is a test."]
        expected_output = [['hello', 'world'], ['this', 'is', 'a', 'test']]
        self.assertEqual(self.processor.process_data(string_list), expected_output)

    def test_process_data2(self):
        string_list = ["12345", "Special@Characters"]
        expected_output = [[], ['specialcharacters']]
        self.assertEqual(self.processor.process_data(string_list), expected_output)

    def test_process_data3(self):
        string_list = []
        expected_output = []
        self.assertEqual(self.processor.process_data(string_list), expected_output)

    def test_process_data4(self):
        string_list = ["Hello World!", "This is a test.", "12345", "Special@Characters"]
        expected_output = [['hello', 'world'], ['this', 'is', 'a', 'test'], [], ['specialcharacters']]
        self.assertEqual(self.processor.process_data(string_list), expected_output)

    def test_process_data5(self):
        string_list = ["Hello World!", "This is a test.", "12345", "Special@Characters", "Hello World!", "This is a test.", "12345", "Special@Characters"]
        expected_output = [['hello', 'world'], ['this', 'is', 'a', 'test'], [], ['specialcharacters'], ['hello', 'world'], ['this', 'is', 'a', 'test'], [], ['specialcharacters']]
        self.assertEqual(self.processor.process_data(string_list), expected_output)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
