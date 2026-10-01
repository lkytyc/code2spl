import re
from collections import Counter

class NLPDataProcessor2:
    """
    The class processes NLP data by extracting words from a list of strings, calculating the frequency of each word, and returning the top 5 most frequent words.
    """


    def process_data(self, string_list):
        """
        keep only English letters and spaces in the string, then convert the string to lower case, and then split the string into a list of words.
        :param string_list: a list of strings
        :return: words_list: a list of words lists
        >>> NLPDataProcessor.process_data(['This is a test.'])
        [['this', 'is', 'a', 'test']]
        """
        words_list = []
        for string in string_list:
            processed_string = string.lower()
            processed_string = re.sub(r'[^a-zA-Z\s]', '', processed_string)
            words = processed_string.split()
            words_list.append(words)
        return words_list

    def calculate_word_frequency(self, words_list):
        """
        Calculate the word frequency of each word in the list of words list, and sort the word frequency dictionary by value in descending order.
        :param words_list: a list of words lists
        :return: top 5 word frequency dictionary, a dictionary of word frequency, key is word, value is frequency
        >>> NLPDataProcessor.calculate_word_frequency([['this', 'is', 'a', 'test'], ['this', 'is', 'another', 'test']])
        {'this': 2, 'is': 2, 'test': 2, 'a': 1, 'another': 1}
        """
        word_frequency = Counter()
        for words in words_list:
            word_frequency.update(words)
        sorted_word_frequency = dict(sorted(word_frequency.items(), key=lambda item: item[1], reverse=True))
        top_5_word_frequency = dict(list(sorted_word_frequency.items())[:5])
        return top_5_word_frequency

    def process(self, string_list):
        """
        keep only English letters and spaces in the string, then convert the string to lower case, and then split the string into a list of words. Calculate the word frequency of each word in the list of words list, and sort the word frequency dictionary by value in descending order.
        :param string_list: a list of strings
        :return: top 5 word frequency dictionary, a dictionary of word frequency, key is word, value is frequency
        >>> NLPDataProcessor.process(['This is a test.', 'This is another test.'])
        {'this': 2, 'is': 2, 'test': 2, 'a': 1, 'another': 1}
        """
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
