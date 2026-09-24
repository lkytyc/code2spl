class Words2Numbers:
    def __init__(self):
        self.numwords = {}

        units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven",
            "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen",
            "fifteen", "sixteen", "seventeen", "eighteen", "nineteen",
        ]
        tens = [
            "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
        ]

        for idx, word in enumerate(units):
            self.numwords[word] = (1, idx)
        for idx, word in enumerate(tens):
            self.numwords[word] = (1, (idx + 2) * 10)

        scales = [
            ("hundred", 100),
            ("thousand", 1000),
            ("million", 1_000_000),
            ("billion", 1_000_000_000),
            ("trillion", 1_000_000_000_000),
        ]
        for word, value in scales:
            self.numwords[word] = (value, 0)

        self.numwords["and"] = (1, 0)

        self.irregular_ordinals = {
            "first": "one",
            "second": "two",
            "third": "three",
            "fifth": "five",
            "eighth": "eight",
            "ninth": "nine",
            "twelfth": "twelve",
        }

        # Each entry: (suffix_to_strip, replacement_to_add)
        self.ordinal_suffixes = [
            ("ieth", "y"),
            ("th", ""),
            ("nd", ""),
            ("rd", ""),
            ("st", ""),
        ]

    def _normalize_word(self, word):
        """Try to convert an ordinal word to its cardinal base form."""
        word = word.lower()
        if word in self.irregular_ordinals:
            return self.irregular_ordinals[word]
        for suffix, replacement in self.ordinal_suffixes:
            if word.endswith(suffix) and len(word) > len(suffix):
                base = word[: len(word) - len(suffix)] + replacement
                if base in self.numwords:
                    return base
        return word

    def text2int(self, text):
        text = text.replace("-", " ")
        words = text.split()

        result_parts = []
        current = 0
        higher = 0

        def flush(val):
            if val != 0:
                result_parts.append(str(val))

        for word in words:
            normalized = self._normalize_word(word)

            if normalized not in self.numwords:
                flush(current + higher)
                current = 0
                higher = 0
                result_parts.append(word)
                continue

            scale, increment = self.numwords[normalized]

            if scale == 1:
                current = current * 1 + increment
            elif scale == 100:
                current = current * scale + increment
            else:
                # thousand and above
                higher += (current + increment) * scale
                current = 0

        flush(higher + current)
        return " ".join(result_parts)

    def is_valid_input(self, text):
        text = text.replace("-", " ")
        words = text.split()

        for word in words:
            normalized = self._normalize_word(word)
            if normalized not in self.numwords:
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
