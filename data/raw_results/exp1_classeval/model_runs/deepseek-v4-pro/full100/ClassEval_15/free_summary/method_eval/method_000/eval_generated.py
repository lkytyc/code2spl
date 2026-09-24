class BoyerMoore:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern

    def match_in_pattern(self, char):
        for i in range(len(self.pattern) - 1, -1, -1):
            if self.pattern[i] == char:
                return i
        return -1

    def mismatch_in_text(self, pos):
        for i in range(len(self.pattern) - 1, -1, -1):
            if pos + i >= len(self.text) or self.pattern[i] != self.text[pos + i]:
                return i
        return -1

    def bad_character_heuristic(self):
        occurrences = []
        pos = 0
        while pos <= len(self.text) - len(self.pattern):
            mismatch_index = self.mismatch_in_text(pos)
            if mismatch_index == -1:
                occurrences.append(pos)
                pos += 1
            else:
                bad_char = self.text[pos + mismatch_index]
                shift = self.match_in_pattern(bad_char)
                if shift == -1:
                    pos += mismatch_index + 1
                else:
                    pos += max(1, mismatch_index - shift)
        return occurrences

import unittest

class BoyerMooreSearchTestMatchInPattern(unittest.TestCase):
    def test_match_in_pattern(self):
        boyerMooreSearch = BoyerMooreSearch("ABAABA", "AB")
        self.assertEqual(boyerMooreSearch.match_in_pattern("A"), 0)

    def test_match_in_pattern_2(self):
        boyerMooreSearch = BoyerMooreSearch("ABAABA", "ABAB")
        self.assertEqual(boyerMooreSearch.match_in_pattern("B"), 3)

    def test_match_in_pattern_3(self):
        boyerMooreSearch = BoyerMooreSearch("ABAABA", "ABCABC")
        self.assertEqual(boyerMooreSearch.match_in_pattern("C"), 5)

    def test_match_in_pattern_4(self):
        boyerMooreSearch = BoyerMooreSearch("ABAABA", "ABCABC")
        self.assertEqual(boyerMooreSearch.match_in_pattern("D"), -1)

    def test_match_in_pattern_5(self):
        boyerMooreSearch = BoyerMooreSearch("ABAABA", "ABCABC")
        self.assertEqual(boyerMooreSearch.match_in_pattern("E"), -1)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
