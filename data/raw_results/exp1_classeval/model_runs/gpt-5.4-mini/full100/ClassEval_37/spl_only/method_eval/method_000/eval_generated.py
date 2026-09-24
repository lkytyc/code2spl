class EncryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_cipher(self, plaintext, shift):
        ciphertext = ""
        for char in plaintext:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                shifted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
                ciphertext += shifted_char
            else:
                ciphertext += char
        return ciphertext

    def vigenere_cipher(self, plain_text):
        encrypted_text = ""
        key_index = 0
        key = self.key
        key_length = len(key)
        for char in plain_text:
            if char.isalpha():
                key_char = key[key_index % key_length].lower()
                shift = ord(key_char) - ord('a')
                lower_char = char.lower()
                encrypted_char = chr((ord(lower_char) - ord('a') + shift) % 26 + ord('a'))
                if char.isupper():
                    encrypted_text += encrypted_char.upper()
                else:
                    encrypted_text += encrypted_char
                key_index += 1
            else:
                encrypted_text += char
        return encrypted_text

    def rail_fence_cipher(self, plain_text, rails):
        fence = [["\n" for _ in range(len(plain_text))] for _ in range(rails)]
        direction = -1
        row = 0
        col = 0
        for _ in plain_text:
            if row == 0 or row == rails - 1:
                direction *= -1
            fence[row][col] = _
            col += 1
            row += direction
        encrypted_text = ""
        for i in range(rails):
            for j in range(len(plain_text)):
                if fence[i][j] != "\n":
                    encrypted_text += fence[i][j]
        return encrypted_text

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
