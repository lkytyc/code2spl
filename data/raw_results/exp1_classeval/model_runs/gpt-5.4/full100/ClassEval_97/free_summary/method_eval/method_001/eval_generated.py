class Words2Numbers:
    def __init__(self):
        self.numwords = {}
        self.units = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
            "eleven": 11,
            "twelve": 12,
            "thirteen": 13,
            "fourteen": 14,
            "fifteen": 15,
            "sixteen": 16,
            "seventeen": 17,
            "eighteen": 18,
            "nineteen": 19,
        }
        self.tens = {
            "twenty": 20,
            "thirty": 30,
            "forty": 40,
            "fifty": 50,
            "sixty": 60,
            "seventy": 70,
            "eighty": 80,
            "ninety": 90,
        }
        self.scales = {
            "hundred": 100,
            "thousand": 1000,
            "million": 1000000,
            "billion": 1000000000,
            "trillion": 1000000000000,
            "quadrillion": 1000000000000000,
            "quintillion": 1000000000000000000,
        }
        self.ordinal_special = {
            "first": "one",
            "second": "two",
            "third": "three",
            "fifth": "five",
            "eighth": "eight",
            "ninth": "nine",
            "twelfth": "twelve",
        }
        self.ordinal_suffixes = ("th", "st", "nd", "rd", "ieth")
        self.numwords.update(self.units)
        self.numwords.update(self.tens)
        self.numwords.update(self.scales)
        self.numwords["and"] = None

    def _normalize_word(self, word):
        if word in self.ordinal_special:
            word = self.ordinal_special[word]
        elif word.endswith("ieth"):
            word = word[:-4] + "y"
        else:
            for suf in ("th", "st", "nd", "rd"):
                if word.endswith(suf) and len(word) > len(suf):
                    base = word[:-len(suf)]
                    if base in self.numwords:
                        word = base
                    break
        return word

    def text2int(self, textnum):
        textnum = textnum.replace("-", " ")
        words = textnum.split()
        current = 0
        result = []

        for raw in words:
            word = raw.lower()
            if word in self.ordinal_special:
                word = self.ordinal_special[word]
            else:
                word = self._normalize_word(word)

            if word in self.numwords and word != "and":
                scale = self.numwords[word]
                if scale is None:
                    continue
                if scale == 100:
                    current = max(1, current) * scale
                elif scale >= 1000:
                    current = max(1, current) * scale
                else:
                    current += scale
            else:
                if current != 0:
                    result.append(str(current))
                    current = 0
                result.append(raw)

        if current != 0:
            result.append(str(current))

        return " ".join(result)

    def is_valid_input(self, textnum):
        textnum = textnum.replace("-", " ")
        words = textnum.split()

        for raw in words:
            word = raw.lower()
            if word in self.ordinal_special:
                continue
            word = self._normalize_word(word)
            if word not in self.numwords and word != "and":
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
