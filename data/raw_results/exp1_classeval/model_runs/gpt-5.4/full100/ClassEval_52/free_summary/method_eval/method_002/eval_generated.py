import string
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('wordnet')


class Lemmatization:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def remove_punctuation(self, sentence):
        return sentence.translate(str.maketrans('', '', string.punctuation))

    def get_pos_tag(self, sentence):
        cleaned_sentence = self.remove_punctuation(sentence)
        tokens = cleaned_sentence.split()
        tagged_tokens = nltk.pos_tag(tokens)
        return [tag for _, tag in tagged_tokens]

    def lemmatize_sentence(self, sentence):
        cleaned_sentence = self.remove_punctuation(sentence)
        tokens = nltk.word_tokenize(cleaned_sentence)
        tagged_tokens = nltk.pos_tag(tokens)
        lemmatized_words = []

        for word, pos in tagged_tokens:
            if pos.startswith('V'):
                lemma = self.lemmatizer.lemmatize(word, pos='v')
            elif pos.startswith('J'):
                lemma = self.lemmatizer.lemmatize(word, pos='a')
            elif pos.startswith('R'):
                lemma = self.lemmatizer.lemmatize(word, pos='r')
            else:
                lemma = self.lemmatizer.lemmatize(word)
            lemmatized_words.append(lemma)

        return lemmatized_words

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
