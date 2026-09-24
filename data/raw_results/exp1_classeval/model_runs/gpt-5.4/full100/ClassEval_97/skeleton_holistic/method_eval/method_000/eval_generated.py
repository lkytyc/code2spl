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

class Words2NumbersTestText2Int(unittest.TestCase):
    def test_text2int(self):
        w2n = Words2Numbers()
        self.assertEqual(w2n.text2int("thirty-two"), "32")

    def test_text2int2(self):
        w2n = Words2Numbers()
        self.assertEqual(w2n.text2int("one hundred and twenty-three"), "123")

    def test_text2int3(self):
        w2n = Words2Numbers()
        self.assertEqual(w2n.text2int("two thousand and nineteen"), "2019")

    def test_text2int4(self):
        w2n = Words2Numbers()
        self.assertEqual(w2n.text2int("one hundred and one"), "101")

    def test_text2int5(self):
        w2n = Words2Numbers()
        self.assertEqual(w2n.text2int("one million and eleven"), "1000011")

    def test_text2int6(self):
        w2n = Words2Numbers()
        self.assertEqual(w2n.text2int("one million one hundred sixty-ninth"), "1000169")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
