class Words2Numbers:
    def __init__(self):
        self.numwords = {}
        self.units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]
        self.tens = [
            "", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
            "eighty", "ninety",
        ]
        self.scales = ["hundred", "thousand", "million", "billion", "trillion"]

        self.numwords["and"] = (1, 0)
        for index, word in enumerate(self.units):
            self.numwords[word] = (1, index)
        for index, word in enumerate(self.tens):
            self.numwords[word] = (1, index * 10)
        for index, word in enumerate(self.scales):
            self.numwords[word] = ((10 ** (index * 3)) if index else 100, 0)

        self.ordinal_words = {
            "first": 1,
            "second": 2,
            "third": 3,
            "fourth": 4,
            "fifth": 5,
            "sixth": 6,
            "seventh": 7,
            "eighth": 8,
            "ninth": 9,
            "tenth": 10,
            "eleventh": 11,
            "twelfth": 12,
            "thirteenth": 13,
            "fourteenth": 14,
            "fifteenth": 15,
            "sixteenth": 16,
            "seventeenth": 17,
            "eighteenth": 18,
            "nineteenth": 19,
            "twentieth": 20,
            "thirtieth": 30,
            "fortieth": 40,
            "fiftieth": 50,
            "sixtieth": 60,
            "seventieth": 70,
            "eightieth": 80,
            "ninetieth": 90,
            "hundredth": 100,
            "thousandth": 1000,
            "millionth": 1000000,
            "billionth": 1000000000,
            "trillionth": 1000000000000,
        }
        self.ordinal_endings = [
            ("ieth", "y"),
            ("th", ""),
            ("st", ""),
            ("nd", ""),
            ("rd", ""),
        ]

    def is_valid_input(self, textnum: str) -> bool:
        textnum = textnum.replace("-", " ")
        for word in textnum.split():
            if word in self.ordinal_words:
                continue
            for ending, replacement in self.ordinal_endings:
                if word.endswith(ending):
                    word = word[: -len(ending)] + replacement
                    break
            if word not in self.numwords:
                return False
        return True

    def text2int(self, textnum: str) -> str:
        textnum = textnum.replace("-", " ")
        current = 0
        result = 0
        curstring = ""
        number_active = False

        for word in textnum.split():
            if word in self.ordinal_words:
                scale = 1
                current += self.ordinal_words[word]
                number_active = True
                continue

            for ending, replacement in self.ordinal_endings:
                if word.endswith(ending):
                    word = word[: -len(ending)] + replacement
                    break

            if word not in self.numwords:
                if number_active:
                    curstring += str(result + current) + " "
                    result = 0
                    current = 0
                    number_active = False
                curstring += word + " "
                continue

            scale, increment = self.numwords[word]
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
            number_active = True

        if number_active:
            curstring += str(result + current)
        else:
            curstring = curstring.rstrip()
        return curstring

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
