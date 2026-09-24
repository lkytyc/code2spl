class Words2Numbers:
    def __init__(self):
        self.number_words = {
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
        self.tens_words = {
            "twenty": 20,
            "thirty": 30,
            "forty": 40,
            "fifty": 50,
            "sixty": 60,
            "seventy": 70,
            "eighty": 80,
            "ninety": 90,
        }
        self.scale_words = {
            "hundred": 100,
            "thousand": 1000,
            "million": 1000000,
            "billion": 1000000000,
            "trillion": 1000000000000,
        }
        self.ordinal_words = {
            "first": 1,
            "second": 2,
            "third": 3,
            "fifth": 5,
            "eighth": 8,
            "ninth": 9,
            "twelfth": 12,
        }
        self.ordinal_endings = ("th", "ieth")

    def _is_ordinal_word(self, word):
        if word in self.ordinal_words:
            return True
        for ending in self.ordinal_endings:
            if word.endswith(ending):
                return True
        return False

    def _token_value(self, word):
        if word in self.number_words:
            return self.number_words[word]
        if word in self.tens_words:
            return self.tens_words[word]
        if word in self.scale_words:
            return self.scale_words[word]
        if word in self.ordinal_words:
            return self.ordinal_words[word]
        return None

    def text2int(self, textnum):
        if textnum is None:
            return ""
        words = textnum.replace("-", " ").split()
        if not words:
            return ""

        result = []
        current = 0
        total_in_phrase = False
        in_number = False
        phrase_words = []

        def flush_phrase():
            nonlocal current, total_in_phrase, in_number, phrase_words
            if in_number:
                value = current if current != 0 or total_in_phrase else 0
                result.append(str(value))
            elif phrase_words:
                result.extend(phrase_words)
            current = 0
            total_in_phrase = False
            in_number = False
            phrase_words = []

        for word in words:
            lw = word.lower()
            val = self._token_value(lw)

            if val is not None:
                if lw in self.ordinal_words or self._is_ordinal_word(lw):
                    if in_number:
                        if lw in self.ordinal_words:
                            current += self.ordinal_words[lw]
                        else:
                            base = lw
                            for ending in self.ordinal_endings:
                                if base.endswith(ending):
                                    base = base[: -len(ending)]
                                    break
                            if base in self.number_words:
                                current += self.number_words[base]
                            elif base in self.tens_words:
                                current += self.tens_words[base]
                            else:
                                current += 0
                        total_in_phrase = True
                    else:
                        result.append(word)
                    continue

                if lw in self.scale_words:
                    in_number = True
                    total_in_phrase = True
                    if current == 0:
                        current = 1
                    if lw == "hundred":
                        current *= 100
                    else:
                        current *= self.scale_words[lw]
                    continue

                in_number = True
                total_in_phrase = True
                current += val
            else:
                if in_number:
                    flush_phrase()
                result.append(word)

        if in_number or phrase_words:
            flush_phrase()

        return " ".join(result)

    def is_valid_input(self, textnum):
        if textnum is None:
            return False
        words = textnum.replace("-", " ").split()
        if not words:
            return False

        for word in words:
            lw = word.lower()
            if lw in self.number_words:
                continue
            if lw in self.tens_words:
                continue
            if lw in self.scale_words:
                continue
            if lw in self.ordinal_words:
                continue
            matched = False
            for ending in self.ordinal_endings:
                if lw.endswith(ending):
                    base = lw[: -len(ending)]
                    if base in self.number_words or base in self.tens_words or base in self.scale_words:
                        matched = True
                        break
                    if base == "":
                        matched = True
                        break
            if matched:
                continue
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

class  Words2NumbersTestMain(unittest.TestCase):
    def test_main(self):
        w2n = Words2Numbers()
        self.assertEqual(w2n.is_valid_input("seventy two thousand and hundred eleven"), True)
        self.assertEqual(w2n.text2int("seventy two thousand and hundred eleven"), "72011")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
