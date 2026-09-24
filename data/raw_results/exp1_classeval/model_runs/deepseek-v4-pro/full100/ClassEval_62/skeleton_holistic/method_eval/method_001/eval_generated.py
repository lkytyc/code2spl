class NLPDataProcessor:
    """
    The class processes NLP data by removing stop words from a list of strings using a pre-defined stop word list.
    """


    def construct_stop_word_list(self):
        """
        Construct a stop word list including 'a', 'an', 'the'.
        :return: a list of stop words
        >>> NLPDataProcessor.construct_stop_word_list()
        ['a', 'an', 'the']
        """
        return ['a', 'an', 'the']

    def remove_stop_words(self, string_list, stop_word_list):
        """
        Remove all the stop words from the list of strings.
        :param string_list: a list of strings
        :param stop_word_list: a list of stop words
        :return: a list of words without stop words
        >>> NLPDataProcessor.process(['This is a test.'])
        [['This', 'is', 'test.']]
        """
        result = []
        for string in string_list:
            words = string.split()
            filtered_words = [word for word in words if word.lower() not in stop_word_list]
            result.append(filtered_words)
        return result

    def process(self, string_list):
        """
        Construct a stop word list including 'a', 'an', 'the', and remove all the stop words from the list of strings.
        :param string_list: a list of strings
        :return: a list of words without stop words
        >>> NLPDataProcessor.process(['This is a test.'])
        [['This', 'is', 'test.']]
        """
        stop_word_list = self.construct_stop_word_list()
        return self.remove_stop_words(string_list, stop_word_list)

import unittest

class NLPDataProcessorTestRemove(unittest.TestCase):
    def setUp(self):
        self.processor = NLPDataProcessor()

    def test_remove_stop_words(self):
        string_list = ['This is a test', 'This is an apple', 'This is the dog']
        stop_word_list = ['a', 'an', 'the']
        words_list = self.processor.remove_stop_words(string_list, stop_word_list)
        expected_words_list = [['This', 'is', 'test'], ['This', 'is', 'apple'], ['This', 'is', 'dog']]
        self.assertEqual(words_list, expected_words_list)

    def test_remove_stop_words_2(self):
        string_list = ['a', 'an', 'the']
        stop_word_list = ['a', 'an', 'the']
        words_list = self.processor.remove_stop_words(string_list, stop_word_list)
        self.assertEqual(words_list, [[], [], []])

    def test_remove_stop_words_3(self):
        string_list = []
        stop_word_list = ['a', 'an', 'the']
        words_list = self.processor.remove_stop_words(string_list, stop_word_list)
        self.assertEqual(words_list, [])

    def test_remove_stop_words_4(self):
        string_list = ['This is a test', 'This is an apple', 'This is the dog']
        stop_word_list = []
        words_list = self.processor.remove_stop_words(string_list, stop_word_list)
        expected_words_list = [['This', 'is', 'a', 'test'], ['This', 'is', 'an', 'apple'], ['This', 'is', 'the', 'dog']]
        self.assertEqual(words_list, expected_words_list)

    def test_remove_stop_words_5(self):
        string_list = ['This is a test', 'This is an apple', 'This is the dog']
        stop_word_list = ['a', 'an', 'the', 'This', 'is']
        words_list = self.processor.remove_stop_words(string_list, stop_word_list)
        expected_words_list = [['is', 'test'], ['is', 'apple'], ['is', 'dog']]
        self.assertEqual(words_list, expected_words_list)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
