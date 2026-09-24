class NLPDataProcessor2:
    def process_data(self, strings):
        cleaned_strings = []
        for s in strings:
            cleaned = ''.join(char for char in s if char.isalpha() or char.isspace())
            cleaned = cleaned.lower()
            words = cleaned.split()
            cleaned_strings.append(words)
        return cleaned_strings

    def calculate_word_frequency(self, word_lists):
        word_count = {}
        for word_list in word_lists:
            for word in word_list:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1
        sorted_words = sorted(word_count.items(), key=lambda item: item[1], reverse=True)
        top_five = dict(sorted_words[:5])
        return top_five

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
