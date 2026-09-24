class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_cipher(self, plaintext, shift):
        shift %= 26
        result = []
        for char in plaintext:
            if 'A' <= char <= 'Z':
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            elif 'a' <= char <= 'z':
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            else:
                result.append(char)
        return ''.join(result)

    def vigenere_cipher(self, plain_text):
        result = []
        key_index = 0
        key = self.key.lower()

        for char in plain_text:
            if char.isalpha():
                shift = ord(key[key_index % len(key)]) - ord('a')
                if 'A' <= char <= 'Z':
                    result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
                else:
                    result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
                key_index += 1
            else:
                result.append(char)

        return ''.join(result)

    def rail_fence_cipher(self, plain_text, rails):
        if rails <= 1:
            return plain_text

        fence = [[] for _ in range(rails)]
        rail = 0
        step = 1

        for char in plain_text:
            fence[rail].append(char)

            if rail == 0:
                step = 1
            elif rail == rails - 1:
                step = -1

            rail += step

        return ''.join(''.join(row) for row in fence)

import unittest

class EncryptionUtilsTestVigenereCipher(unittest.TestCase):
    def test_vigenere_cipher(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.vigenere_cipher("abc"), "kfa")

    def test_vigenere_cipher_2(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.vigenere_cipher("hello"), "rijvs")

    def test_vigenere_cipher_3(self):
        encryption_utils = EncryptionUtils("longkey")
        self.assertEqual(encryption_utils.vigenere_cipher("AbCdEfG"), "LpPjOjE")

    def test_vigenere_cipher_4(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.vigenere_cipher("Hello, World! 123"), "Rijvs, Uyvjn! 123")

    def test_vigenere_cipher_5(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.vigenere_cipher(""), "")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
