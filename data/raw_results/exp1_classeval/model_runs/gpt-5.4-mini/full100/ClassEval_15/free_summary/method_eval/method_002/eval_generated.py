class BoyerMooreSearch:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern
        self.text_len = len(text)
        self.pattern_len = len(pattern)

    def match_in_pattern(self, char):
        for i in range(self.pattern_len - 1, -1, -1):
            if self.pattern[i] == char:
                return i
        return -1

    def mismatch_in_text(self, currentPos):
        j = self.pattern_len - 1
        while j >= 0:
            if currentPos + j >= self.text_len or self.text[currentPos + j] != self.pattern[j]:
                return currentPos + j
            j -= 1
        return -1

    def bad_character_heuristic(self):
        results = []
        if self.pattern_len == 0:
            return list(range(self.text_len + 1))

        currentPos = 0
        while currentPos <= self.text_len - self.pattern_len:
            mismatch_index = self.mismatch_in_text(currentPos)
            if mismatch_index == -1:
                results.append(currentPos)
                currentPos += 1
            else:
                mismatch_char = self.text[mismatch_index]
                last_match_index = self.match_in_pattern(mismatch_char)
                shift = max(1, (mismatch_index - currentPos) - last_match_index)
                currentPos += shift
        return results

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
