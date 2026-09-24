class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_cipher(self, plaintext, shift):
        ciphertext = ""
        for char in plaintext:
            if char.isalpha():
                if char.isupper():
                    ascii_offset = 65
                else:
                    ascii_offset = 97
                shifted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
                ciphertext += shifted_char
            else:
                ciphertext += char
        return ciphertext

    def vigenere_cipher(self, plain_text):
        encrypted_text = ""
        key_index = 0
        for char in plain_text:
            if char.isalpha():
                shift = ord(self.key[key_index % len(self.key)].lower()) - ord('a')
                encrypted_char = chr((ord(char.lower()) - ord('a') + shift) % 26 + ord('a'))
                if char.isupper():
                    encrypted_text += encrypted_char.upper()
                else:
                    encrypted_text += encrypted_char
                key_index += 1
            else:
                encrypted_text += char
        return encrypted_text

    def rail_fence_cipher(self, plain_text, rails):
        fence = [['\n' for _ in range(len(plain_text))] for _ in range(rails)]
        direction = -1
        row = 0
        col = 0
        for char in plain_text:
            if row == 0 or row == rails - 1:
                direction = -direction
            fence[row][col] = char
            col += 1
            row += direction
        encrypted_text = ""
        for i in range(rails):
            for j in range(len(plain_text)):
                if fence[i][j] != '\n':
                    encrypted_text += fence[i][j]
        return encrypted_text

import unittest

class EncryptionUtilsTestRailFenceCipher(unittest.TestCase):
    def test_rail_fence_cipher(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.rail_fence_cipher("abc", 2), "acb")

    def test_rail_fence_cipher_2(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.rail_fence_cipher("hello", 2), "hloel")

    def test_rail_fence_cipher_3(self):
        encryption_utils = EncryptionUtils("longkey")
        self.assertEqual(encryption_utils.rail_fence_cipher("AbCdEfG", 2), "ACEGbdf")

    def test_rail_fence_cipher_4(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.rail_fence_cipher("Hello, World! 123", 2), "Hlo ol!13el,Wrd 2")

    def test_rail_fence_cipher_5(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.rail_fence_cipher("", 2), "")

    def test_rail_fence_cipher_6(self):
        encryption_utils = EncryptionUtils("key")
        self.assertEqual(encryption_utils.rail_fence_cipher("abcdefg", 3), "aebdfcg")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
