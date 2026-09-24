class Manacher:
    def __init__(self, input_string):
        self.input_string = input_string

    def palindromic_length(self, center, diff, string):
        if (center - diff < 0 or
                center + diff >= len(string) or
                string[center - diff] != string[center + diff]):
            return 0
        return 1 + self.palindromic_length(center, diff + 1, string)

    def palindromic_string(self):
        if not self.input_string:
            return self.input_string

        # Transform: insert '|' between every character
        transformed = '|'.join(self.input_string)

        max_length = 0
        max_center = 0

        for i in range(len(transformed)):
            length = self.palindromic_length(i, 1, transformed)
            if length > max_length:
                max_length = length
                max_center = i

        start = max_center - max_length
        end = max_center + max_length + 1
        substring = transformed[start:end]

        return substring.replace('|', '')

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


class ManacherTestPalindromicString(unittest.TestCase):
    def test_palindromic_string(self):
        manacher = Manacher('ababaxse')
        self.assertEqual(manacher.palindromic_string(), 'ababa')

    def test_palindromic_string_2(self):
        manacher = Manacher('ababax')
        self.assertEqual(manacher.palindromic_string(), 'ababa')

    def test_palindromic_string_3(self):
        manacher = Manacher('ababax')
        self.assertEqual(manacher.palindromic_string(), 'ababa')

    def test_palindromic_string_4(self):
        manacher = Manacher('ababaxssss')
        self.assertEqual(manacher.palindromic_string(), 'ababa')

    def test_palindromic_string_5(self):
        manacher = Manacher('abab')
        self.assertEqual(manacher.palindromic_string(), 'aba')


class ManacherTestMain(unittest.TestCase):
    def test_main(self):
        manacher = Manacher('ababa')
        self.assertEqual(manacher.palindromic_length(2, 1, 'a|b|a|b|a'), 2)
        self.assertEqual(manacher.palindromic_string(), 'ababa')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
