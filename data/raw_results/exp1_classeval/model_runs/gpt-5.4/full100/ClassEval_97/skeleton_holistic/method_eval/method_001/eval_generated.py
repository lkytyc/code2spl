class Words2Numbers:
    """
    The class provides a text-to-number conversion utility, allowing conversion of written numbers (in words) to their numerical representation.
    """

    def __init__(self):
        """
        Initialize the word lists and dictionaries required for conversion
        """
        self.numwords = {}
        self.units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]
        self.tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        self.scales = ["hundred", "thousand", "million", "billion", "trillion"]

        self.numwords["and"] = (1, 0)
        for idx, word in enumerate(self.units):
            self.numwords[word] = (1, idx)
        for idx, word in enumerate(self.tens):
            self.numwords[word] = (1, idx * 10)
        for idx, word in enumerate(self.scales):
            self.numwords[word] = (10 ** (idx * 3 or 2), 0)

        self.ordinal_words = {'first': 1, 'second': 2, 'third': 3, 'fifth': 5, 'eighth': 8, 'ninth': 9, 'twelfth': 12}
        self.ordinal_endings = [('ieth', 'y'), ('th', '')]

    def text2int(self, textnum):
        """
        Convert the word string to the corresponding integer string
        :param textnum: string, the word string to be converted
        :return: string, the final converted integer string
        >>> w2n = Words2Numbers()
        >>> w2n.text2int("thirty-two")
        "32"
        """
        if not isinstance(textnum, str):
            raise TypeError("Input must be a string")

        textnum = textnum.strip().lower()
        if not textnum:
            raise ValueError("Input cannot be empty")

        current = result = 0
        words = textnum.replace("-", " ").split()

        for word in words:
            if word in self.ordinal_words:
                scale, increment = 1, self.ordinal_words[word]
            else:
                normalized = word
                if normalized not in self.numwords:
                    for ending, replacement in self.ordinal_endings:
                        if normalized.endswith(ending):
                            candidate = normalized[:-len(ending)] + replacement
                            if candidate in self.numwords:
                                normalized = candidate
                                break
                if normalized not in self.numwords:
                    raise ValueError("Illegal word: " + word)
                scale, increment = self.numwords[normalized]

            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0

        return str(result + current)

    def is_valid_input(self, textnum):
        """
        Check if the input text contains only valid words that can be converted into numbers.
        :param textnum: The input text containing words representing numbers.
        :return: True if input is valid, False otherwise.
        >>> w2n = Words2Numbers()
        >>> w2n.is_valid_input("thirty-two")
        False
        """
        if not isinstance(textnum, str):
            return False

        textnum = textnum.strip().lower()
        if not textnum or "-" in textnum:
            return False

        words = textnum.split()
        if not words:
            return False

        for word in words:
            if word in self.numwords or word in self.ordinal_words:
                continue

            valid = False
            for ending, replacement in self.ordinal_endings:
                if word.endswith(ending):
                    candidate = word[:-len(ending)] + replacement
                    if candidate in self.numwords:
                        valid = True
                        break
            if not valid:
                return False

        return True

import unittest

class Words2NumbersTestIsValidInput(unittest.TestCase):
    def test_is_valid_input(self):
        w2n = Words2Numbers()
        self.assertTrue(w2n.is_valid_input("twenty-five thousand three hundred and forty-two"))

    def test_is_valid_input2(self):
        w2n = Words2Numbers()
        self.assertTrue(w2n.is_valid_input("second hundred and third"))

    def test_is_valid_input3(self):
        w2n = Words2Numbers()
        self.assertTrue(w2n.is_valid_input("twenty-fifth thousand three hundred and forty-second"))

    def test_is_valid_input4(self):
        w2n = Words2Numbers()
        self.assertFalse(w2n.is_valid_input("eleventy thousand and five"))

    def test_is_valid_input5(self):
        w2n = Words2Numbers()
        self.assertTrue(w2n.is_valid_input("seventy two thousand and hundred eleven"))

    def test_is_valid_input6(self):
        w2n = Words2Numbers()
        self.assertTrue(w2n.is_valid_input("fifteenth hundred"))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
