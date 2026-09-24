import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import string

class Lemmatization:
    def __init__(self):
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        self.lemmatizer = WordNetLemmatizer()

    def remove_punctuation(self, sentence):
        return sentence.translate(str.maketrans('', '', string.punctuation))

    def _get_wordnet_pos(self, treebank_tag):
        if treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def lemmatize_sentence(self, sentence):
        cleaned = self.remove_punctuation(sentence)
        words = nltk.word_tokenize(cleaned)
        pos_tags = nltk.pos_tag(words)
        lemmatized_words = []
        for word, tag in pos_tags:
            wn_pos = self._get_wordnet_pos(tag)
            lemmatized_words.append(self.lemmatizer.lemmatize(word, pos=wn_pos))
        return lemmatized_words

    def get_pos_tag(self, sentence):
        cleaned = self.remove_punctuation(sentence)
        words = nltk.word_tokenize(cleaned)
        pos_tags = nltk.pos_tag(words)
        return [tag for _, tag in pos_tags]

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
