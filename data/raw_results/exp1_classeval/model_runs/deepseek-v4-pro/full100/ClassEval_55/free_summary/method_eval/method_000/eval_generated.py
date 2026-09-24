class Manacher:
    def __init__(self, input_string):
        self.input_string = input_string

    def palindromic_length(self, center, diff, string):
        if center - diff == -1 or center + diff == len(string) or string[center - diff] != string[center + diff]:
            return 0
        return 1 + self.palindromic_length(center, diff + 1, string)

    def palindromic_string(self):
        if not self.input_string:
            return ""
        modified = "|" + "|".join(self.input_string) + "|"
        max_center = 0
        max_radius = 0
        for center in range(len(modified)):
            radius = self.palindromic_length(center, 1, modified)
            if radius > max_radius:
                max_radius = radius
                max_center = center
        start = max_center - max_radius
        end = max_center + max_radius
        palindrome = modified[start:end + 1]
        return palindrome.replace("|", "")

import unittest

class ManacherTestPalindromicLength(unittest.TestCase):
    def test_palindromic_length(self):
        manacher = Manacher('ababa')
        self.assertEqual(manacher.palindromic_length(2, 1, 'a|b|a|b|a'), 2)
    def test_palindromic_length_2(self):
        manacher = Manacher('ababaxse')
        self.assertEqual(manacher.palindromic_length(2, 1, 'a|b|a|b|a|x|s|e'), 2)

    def test_palindromic_length_3(self):
        manacher = Manacher('ababax')
        self.assertEqual(manacher.palindromic_length(2, 3, 'a|b|a|b|a|x'), 0)

    def test_palindromic_length_4(self):
        manacher = Manacher('ababax')
        self.assertEqual(manacher.palindromic_length(9, 2, 'a|b|a|b|a|x'), 0)

    def test_palindromic_length_5(self):
        manacher = Manacher('ababax')
        self.assertEqual(manacher.palindromic_length(4, 1, 'a|b|a|b|a|x'), 4)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
