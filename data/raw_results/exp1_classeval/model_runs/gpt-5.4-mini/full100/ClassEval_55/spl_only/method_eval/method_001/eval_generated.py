class Manacher:
    def __init__(self, input_string):
        self.input_string = input_string

    def palindromic_length(self, center, diff, string):
        if (
            center - diff < 0
            or center + diff >= len(string)
            or string[center - diff] != string[center + diff]
        ):
            return 0
        return 1 + self.palindromic_length(center, diff + 1, string)

    def palindromic_string(self):
        max_length = 0
        new_input_string = ""
        output_string = ""

        if not self.input_string:
            return output_string

        for i, ch in enumerate(self.input_string):
            new_input_string += ch
            if i != len(self.input_string) - 1:
                new_input_string += "|"

        start = 0
        for i in range(len(new_input_string)):
            length = self.palindromic_length(i, 1, new_input_string)
            if length > max_length:
                max_length = length
                start = i

        for ch in new_input_string[start - max_length : start + max_length + 1]:
            if ch != "|":
                output_string += ch

        return output_string

import unittest

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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
