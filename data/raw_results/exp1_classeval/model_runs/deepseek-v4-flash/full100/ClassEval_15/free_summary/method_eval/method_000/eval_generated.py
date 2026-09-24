class BoyerMooreSearch:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern

    def match_in_pattern(self, char):
        return self.pattern.rfind(char)

    def mismatch_in_text(self, alignment):
        for i in range(len(self.pattern) - 1, -1, -1):
            if self.pattern[i] != self.text[alignment + i]:
                return alignment + i
        return -1

    def bad_character_heuristic(self):
        positions = []
        for alignment in range(len(self.text) - len(self.pattern) + 1):
            mismatch = self.mismatch_in_text(alignment)
            if mismatch == -1:
                positions.append(alignment)
            else:
                bad_char = self.text[mismatch]
                shift = (mismatch - alignment) - self.match_in_pattern(bad_char)
                if shift < 1:
                    shift = 1
                alignment += shift
        return positions

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
