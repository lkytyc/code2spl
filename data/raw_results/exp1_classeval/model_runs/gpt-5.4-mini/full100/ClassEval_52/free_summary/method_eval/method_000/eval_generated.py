import string
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download("averaged_perceptron_tagger")
nltk.download("punkt")
nltk.download("wordnet")


class Lemmatization:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def remove_punctuation(self, sentence):
        return sentence.translate(str.maketrans("", "", string.punctuation))

    def lemmatize_sentence(self, sentence):
        cleaned_sentence = self.remove_punctuation(sentence)
        tokens = nltk.word_tokenize(cleaned_sentence)
        tagged_tokens = nltk.pos_tag(tokens)

        lemmatized_words = []
        for word, tag in tagged_tokens:
            if tag.startswith("V"):
                lemma = self.lemmatizer.lemmatize(word, pos="v")
            elif tag.startswith("J"):
                lemma = self.lemmatizer.lemmatize(word, pos="a")
            elif tag.startswith("R"):
                lemma = self.lemmatizer.lemmatize(word, pos="r")
            else:
                lemma = self.lemmatizer.lemmatize(word)
            lemmatized_words.append(lemma)

        return lemmatized_words

    def get_pos_tag(self, sentence):
        cleaned_sentence = self.remove_punctuation(sentence)
        tokens = nltk.word_tokenize(cleaned_sentence)
        tagged_tokens = nltk.pos_tag(tokens)
        return [tag for _, tag in tagged_tokens]

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
