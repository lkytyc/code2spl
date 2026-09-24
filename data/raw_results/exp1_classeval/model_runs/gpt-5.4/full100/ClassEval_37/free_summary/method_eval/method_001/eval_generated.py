class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_cipher(self, plaintext, shift):
        encrypted = []
        for char in plaintext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                encrypted_char = chr((ord(char) - base + shift) % 26 + base)
                encrypted.append(encrypted_char)
            else:
                encrypted.append(char)
        return ''.join(encrypted)

    def vigenere_cipher(self, plain_text):
        if not self.key:
            return plain_text

        encrypted = []
        key_index = 0
        key = self.key

        for char in plain_text:
            if char.isalpha():
                key_char = key[key_index % len(key)]
                shift = ord(key_char.lower()) - ord('a')
                base = ord('A') if char.isupper() else ord('a')
                encrypted_char = chr((ord(char) - base + shift) % 26 + base)
                encrypted.append(encrypted_char)
                key_index += 1
            else:
                encrypted.append(char)

        return ''.join(encrypted)

    def rail_fence_cipher(self, plain_text, rails):
        if rails <= 1 or rails >= len(plain_text):
            return plain_text

        fence = ['' for _ in range(rails)]
        rail = 0
        direction = 1

        for char in plain_text:
            fence[rail] += char
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction

        return ''.join(fence)

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
