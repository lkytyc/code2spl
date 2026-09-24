import re
from collections import Counter

class NLPDataProcessor2:
    def process_data(self, string_list):
        words_list = []
        for text in string_list:
            cleaned = re.sub(r'[^a-zA-Z\s]', '', text)
            words = cleaned.lower().split()
            words_list.append(words)
        return words_list

    def calculate_word_frequency(self, words_list):
        word_counts = Counter()
        for words in words_list:
            word_counts.update(words)
        sorted_counts = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_counts[:5])

    def process(self, string_list):
        words_list = self.process_data(string_list)
        return self.calculate_word_frequency(words_list)

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
