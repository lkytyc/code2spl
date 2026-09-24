import string
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag

nltk.download('averaged_perceptron_tagger_eng', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('wordnet', quiet=True)


class Lemmatization:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def remove_punctuation(self, sentence):
        translator = str.maketrans('', '', string.punctuation)
        return sentence.translate(translator)

    def get_pos_tag(self, sentence):
        sentence = self.remove_punctuation(sentence)
        tokens = word_tokenize(sentence)
        tags = pos_tag(tokens)
        return [tag for _, tag in tags]

    def lemmatize_sentence(self, sentence):
        sentence = self.remove_punctuation(sentence)
        tokens = word_tokenize(sentence)
        tagged = pos_tag(tokens)
        lemmatized = []
        for word, tag in tagged:
            if tag.startswith('VB'):
                pos = 'v'
            elif tag.startswith('JJ'):
                pos = 'a'
            elif tag.startswith('RB'):
                pos = 'r'
            else:
                pos = 'n'
            lemmatized.append(self.lemmatizer.lemmatize(word, pos=pos))
        return lemmatized

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
