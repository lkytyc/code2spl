class BoyerMooreSearch:
    def __init__(self, text: str, pattern: str):
        self.text = text
        self.pattern = pattern
        self.textLen = len(text)
        self.patLen = len(pattern)

    def bad_character_heuristic(self):
        positions = []
        for i in range(0, self.textLen - self.patLen + 1):
            mismatch_index = self.mismatch_in_text(i)
            if mismatch_index == -1:
                positions.append(i)
            if mismatch_index != -1:
                match_index = self.match_in_pattern(self.text[mismatch_index])
                i = mismatch_index - match_index
        return positions

    def match_in_pattern(self, char: str) -> int:
        for i in range(self.patLen - 1, -1, -1):
            if char == self.pattern[i]:
                return i
        return -1

    def mismatch_in_text(self, currentPos: int) -> int:
        for i in range(self.patLen - 1, -1, -1):
            if self.pattern[i] != self.text[currentPos + i]:
                return currentPos + i
        return -1

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
