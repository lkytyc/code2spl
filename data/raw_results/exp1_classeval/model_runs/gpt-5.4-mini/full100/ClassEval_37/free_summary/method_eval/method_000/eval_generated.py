class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_cipher(self, plaintext, shift):
        result = []
        shift %= 26
        for ch in plaintext:
            if 'a' <= ch <= 'z':
                result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
            elif 'A' <= ch <= 'Z':
                result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
            else:
                result.append(ch)
        return ''.join(result)

    def vigenere_cipher(self, plain_text):
        if not self.key:
            return plain_text

        result = []
        key = self.key
        key_len = len(key)
        key_index = 0

        for ch in plain_text:
            if ch.isalpha():
                k = key[key_index % key_len]
                if k.isalpha():
                    shift = ord(k.lower()) - ord('a')
                else:
                    shift = 0

                if 'a' <= ch <= 'z':
                    result.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
                else:
                    result.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
                key_index += 1
            else:
                result.append(ch)

        return ''.join(result)

    def rail_fence_cipher(self, plain_text, rails):
        if rails <= 1 or len(plain_text) <= 1:
            return plain_text

        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1

        for ch in plain_text:
            fence[rail].append(ch)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction

        return ''.join(''.join(row) for row in fence)

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
