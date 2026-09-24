class Manacher:
    def __init__(self, s):
        self.s = s

    def palindromic_length(self, center, diff, string):
        if center - diff < 0 or center + diff >= len(string):
            return 0
        if string[center - diff] != string[center + diff]:
            return 0
        return 1 + self.palindromic_length(center, diff + 1, string)

    def palindromic_string(self):
        if not self.s:
            return ""
        transformed = '|' + '|'.join(self.s) + '|'
        max_len = 0
        max_center = 0
        for i in range(len(transformed)):
            length = self.palindromic_length(i, 1, transformed)
            if length > max_len:
                max_len = length
                max_center = i
        start = max_center - max_len
        end = max_center + max_len
        result = transformed[start:end+1]
        result = result.replace('|', '')
        return result

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
