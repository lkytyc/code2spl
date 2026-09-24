import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
import string


nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('wordnet')

class Lemmatization:
    """
    This is a class about Lemmatization, which utilizes the nltk library to perform lemmatization and part-of-speech tagging on sentences, as well as remove punctuation.
    """

    def __init__(self):
        """
        creates a WordNetLemmatizer object and stores it in the self.lemmatizer member variable.
        """
        self.lemmatizer = WordNetLemmatizer()

    def lemmatize_sentence(self, sentence):
        """
        Remove punctuations of the sentence and tokenizes the input sentence, mark the part of speech tag of each word,
        lemmatizes the words with different parameters based on their parts of speech, and stores in a list.
        :param sentence: a sentence str
        :return: a list of words which have been lemmatized.
        >>> lemmatization = Lemmatization()
        >>> lemmatization.lemmatize_sentence("I am running in a race.")
        ['I', 'be', 'run', 'in', 'a', 'race']

        """
        lemmatized_words = []
        sentence = self.remove_punctuation(sentence)
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)
        for word, tag in tagged_words:
            if tag.startswith('V'):
                lemmatized_word = self.lemmatizer.lemmatize(word, pos='v')
            elif tag.startswith('J'):
                lemmatized_word = self.lemmatizer.lemmatize(word, pos='a')
            elif tag.startswith('R'):
                lemmatized_word = self.lemmatizer.lemmatize(word, pos='r')
            else:
                lemmatized_word = self.lemmatizer.lemmatize(word)
            lemmatized_words.append(lemmatized_word)
        return lemmatized_words

    def get_pos_tag(self, sentence):
        """
        Remove punctuations of the sentence and tokenizes the input sentence, mark the part of speech tag of each word.
        :param sentence: a sentence str
        :return: list, part of speech tag of each word in the sentence.
        >>> lemmatization = Lemmatization()
        >>> lemmatization.get_pos_tag("I am running in a race.")
        ['PRP', 'VBP', 'VBG', 'IN', 'DT', 'NN']

        """
        pos_tags = []
        sentence = self.remove_punctuation(sentence)
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)
        for tagged_word in tagged_words:
            pos_tags.append(tagged_word[1])
        return pos_tags

    def remove_punctuation(self, sentence):
        """
        Removes punctuation from the input text.
        :param sentence: a sentence str
        :return: str, sentence without any punctuation
        >>> lemmatization = Lemmatization()
        >>> lemmatization.remove_punctuation("I am running in a race.")
        'I am running in a race'

        """
        return sentence.translate(str.maketrans('', '', string.punctuation))

import unittest

class LemmatizationTestRemovePunctuation(unittest.TestCase):
    def test_remove_punctuation_1(self):
        lemmatization = Lemmatization()
        result = lemmatization.remove_punctuation("I am running in a race.")
        expected = "I am running in a race"
        self.assertEqual(result, expected)

    def test_remove_punctuation_2(self):
        lemmatization = Lemmatization()
        result = lemmatization.remove_punctuation("Until the beating, Cantanco's eyesight had been weak, but adequate.")
        expected = 'Until the beating Cantancos eyesight had been weak but adequate'
        self.assertEqual(result, expected)

    def test_remove_punctuation_3(self):
        lemmatization = Lemmatization()
        result = lemmatization.remove_punctuation("The dog's barked at the mailman!!!")
        expected = 'The dogs barked at the mailman'
        self.assertEqual(result, expected)

    def test_remove_punctuation_4(self):
        lemmatization = Lemmatization()
        result = lemmatization.remove_punctuation("He was running and eating at same time... ")
        expected = 'He was running and eating at same time '
        self.assertEqual(result, expected)

    def test_remove_punctuation_5(self):
        lemmatization = Lemmatization()
        result = lemmatization.remove_punctuation("Is this a test? I hope it is...")
        expected = 'Is this a test I hope it is'
        self.assertEqual(result, expected)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
