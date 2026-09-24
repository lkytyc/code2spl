import nltk
import string
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)


class Lemmatization:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.translator = str.maketrans('', '', string.punctuation)

    def remove_punctuation(self, sentence):
        return sentence.translate(self.translator)

    def get_pos_tag(self, sentence):
        sentence = self.remove_punctuation(sentence)
        words = word_tokenize(sentence)
        tagged = pos_tag(words)
        return [tag for _, tag in tagged]

    def _get_wordnet_pos(self, tag):
        if tag.startswith('V'):
            return wordnet.VERB
        if tag.startswith('J'):
            return wordnet.ADJ
        if tag.startswith('R'):
            return wordnet.ADV
        return wordnet.NOUN

    def lemmatize_sentence(self, sentence):
        sentence = self.remove_punctuation(sentence)
        words = word_tokenize(sentence)
        tagged = pos_tag(words)
        return [self.lemmatizer.lemmatize(word, self._get_wordnet_pos(tag)) for word, tag in tagged]

import unittest

class LemmatizationTestLemmatizeSentence(unittest.TestCase):
    def test_lemmatize_sentence_1(self):
        lemmatization = Lemmatization()
        result = lemmatization.lemmatize_sentence("I am running in a race.")
        expected = ['I', 'be', 'run', 'in', 'a', 'race']
        self.assertEqual(result, expected)

    def test_lemmatize_sentence_2(self):
        lemmatization = Lemmatization()
        result = lemmatization.lemmatize_sentence("Until the beating, Cantanco's eyesight had been weak, but adequate.")
        expected = ['Until', 'the', 'beating', 'Cantancos', 'eyesight', 'have', 'be', 'weak', 'but', 'adequate']
        self.assertEqual(result, expected)

    def test_lammatize_sentence_3(self):
        lemmatization = Lemmatization()
        result = lemmatization.lemmatize_sentence("The dog's barked at the mailman.")
        expected = ['The', 'dog', 'bark', 'at', 'the', 'mailman']
        self.assertEqual(result, expected)

    def test_lemmatize_sentence_4(self):
        lemmatization = Lemmatization()
        result = lemmatization.lemmatize_sentence("He was running and eating at same time. ")
        expected = ['He', 'be', 'run', 'and', 'eat', 'at', 'same', 'time']
        self.assertEqual(result, expected)

    def test_lemmatize_sentence_5(self):
        lemmatization = Lemmatization()
        result = lemmatization.lemmatize_sentence("I was taking a ride in the car.")
        expected = ['I', 'be', 'take', 'a', 'ride', 'in', 'the', 'car']
        self.assertEqual(result, expected)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
