class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_cipher(self, plaintext, shift):
        result = []
        for ch in plaintext:
            if 'a' <= ch <= 'z':
                result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
            elif 'A' <= ch <= 'Z':
                result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(ch)
        return ''.join(result)

    def vigenere_cipher(self, plaintext):
        key = ''.join(c for c in self.key if 'a' <= c <= 'z' or 'A' <= c <= 'Z').lower()
        if not key:
            return plaintext

        result = []
        key_index = 0
        for ch in plaintext:
            if 'a' <= ch <= 'z':
                shift = ord(key[key_index % len(key)]) - ord('a')
                result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
                key_index += 1
            elif 'A' <= ch <= 'Z':
                shift = ord(key[key_index % len(key)]) - ord('a')
                result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
                key_index += 1
            else:
                result.append(ch)
        return ''.join(result)

    def rail_fence_cipher(self, plain_text, rails):
        if rails <= 1:
            return plain_text

        fence = [''] * rails
        rail = 0
        step = 1

        for ch in plain_text:
            fence[rail] += ch
            if rail == 0:
                step = 1
            elif rail == rails - 1:
                step = -1
            rail += step

        return ''.join(fence)

import unittest

class EncryptionUtilsTestCaesarCipher(unittest.TestCase):
    def test_caesar_cipher(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.caesar_cipher("abc", 1), "bcd")

    def test_caesar_cipher_2(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.caesar_cipher("WORLD", -2), "UMPJB")

    def test_caesar_cipher_3(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.caesar_cipher("", 4), "")

    def test_caesar_cipher_4(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.caesar_cipher("abcxyz", 26), "abcxyz")

    def test_caesar_cipher_5(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.caesar_cipher("abcxyz", 27), "bcdyza")

    def test_caesar_cipher_6(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.caesar_cipher("123", 27), "123")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
