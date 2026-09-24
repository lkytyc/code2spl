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
