import string

class LongestWord:
    def __init__(self):
        self.word_list = []

    def add_word(self, word):
        self.word_list.append(word)

    def find_longest_word(self, sentence):
        sentence = sentence.lower()
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        tokens = sentence.split(' ')

        longest = ''
        for token in tokens:
            if token in self.word_list and len(token) > len(longest):
                longest = token

        return longest

import unittest

class LongestWordTestFindLongestWord(unittest.TestCase):
    def test_find_longest_word_1(self):
        longestWord = LongestWord()
        longestWord.add_word("a")
        sentence = 'I am a student.'
        self.assertEqual('a', longestWord.find_longest_word(sentence))

    def test_find_longest_word_2(self):
        longestWord = LongestWord()
        sentence = 'I am a student.'
        self.assertEqual('', longestWord.find_longest_word(sentence))

    def test_find_longest_word_3(self):
        longestWord = LongestWord()
        longestWord.add_word("student")
        sentence = 'I am a student.'
        self.assertEqual('student', longestWord.find_longest_word(sentence))

    def test_find_longest_word_4(self):
        longestWord = LongestWord()
        longestWord.add_word("apple")
        sentence = 'Apple is red.'
        self.assertEqual('apple', longestWord.find_longest_word(sentence))

    def test_find_longest_word_5(self):
        longestWord = LongestWord()
        longestWord.add_word("apple")
        longestWord.add_word("red")
        sentence = 'Apple is red.'
        self.assertEqual('apple', longestWord.find_longest_word(sentence))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
