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

class LemmatizationTestGetPosTag(unittest.TestCase):
    def test_get_pos_tag_1(self):
        lemmatization = Lemmatization()
        result = lemmatization.get_pos_tag("I am running in a race.")
        expected = ['PRP', 'VBP', 'VBG', 'IN', 'DT', 'NN']
        self.assertEqual(result, expected)

    def test_get_pos_tag_2(self):
        lemmatization = Lemmatization()
        result = lemmatization.get_pos_tag("Cantanco's eyesight had been weak, but adequate.")
        expected = ['NNP', 'NN', 'VBD', 'VBN', 'JJ', 'CC', 'JJ']
        self.assertEqual(result, expected)

    def test_get_pos_tag_3(self):
        lemmatization = Lemmatization()
        result = lemmatization.get_pos_tag("The dog's barked at the mailman.")
        expected = ['DT', 'NNS', 'VBD', 'IN', 'DT', 'NN']
        self.assertEqual(result, expected)

    def test_get_pos_tag_4(self):
        lemmatization = Lemmatization()
        result = lemmatization.get_pos_tag("He was running and eating at same time. ")
        expected = ['PRP', 'VBD', 'VBG', 'CC', 'VBG', 'IN', 'JJ', 'NN']
        self.assertEqual(result, expected)

    def test_get_pos_tag_5(self):
        lemmatization = Lemmatization()
        result = lemmatization.get_pos_tag("I was taking a ride in the car.")
        expected = ['PRP', 'VBD', 'VBG', 'DT', 'NN', 'IN', 'DT', 'NN']
        self.assertEqual(result, expected)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
