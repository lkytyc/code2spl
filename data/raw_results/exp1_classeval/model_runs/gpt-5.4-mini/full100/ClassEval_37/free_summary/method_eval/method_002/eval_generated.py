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
