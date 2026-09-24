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

class BoyerMooreSearchTestBadCharacterHeuristic(unittest.TestCase):
    def test_bad_character_heuristic(self):
        boyerMooreSearch = BoyerMooreSearch("ABAABA", "AB")
        self.assertEqual(boyerMooreSearch.bad_character_heuristic(), [0, 3])

    def test_bad_character_heuristic_2(self):
        boyerMooreSearch = BoyerMooreSearch("ABAABA", "ABC")
        self.assertEqual(boyerMooreSearch.bad_character_heuristic(), [])

    def test_bad_character_heuristic_3(self):
        boyerMooreSearch = BoyerMooreSearch("ABAABA", "")
        self.assertEqual(boyerMooreSearch.bad_character_heuristic(), [0, 1, 2, 3, 4, 5, 6])

    def test_bad_character_heuristic_4(self):
        boyerMooreSearch = BoyerMooreSearch("ABACABA", "ABA")
        self.assertEqual(boyerMooreSearch.bad_character_heuristic(), [0, 4])

    def test_bad_character_heuristic_5(self):
        boyerMooreSearch = BoyerMooreSearch("ABACABA", "ABAC")
        self.assertEqual(boyerMooreSearch.bad_character_heuristic(), [0])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
