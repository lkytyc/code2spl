class DecryptionUtils:
    def __init__(self, key):
        self.key = ''.join(ch for ch in key if ch.isalpha()).lower()

    def caesar_decipher(self, ciphertext, shift):
        shift = shift % 26
        result = []
        for ch in ciphertext:
            if ch.isalpha():
                if ch.isupper():
                    result.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
                else:
                    result.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
            else:
                result.append(ch)
        return ''.join(result)

    def vigenere_decipher(self, ciphertext):
        if not self.key:
            return ciphertext

        key = self.key
        key_len = len(key)
        key_index = 0
        result = []

        for ch in ciphertext:
            if ch.isalpha():
                shift = ord(key[key_index % key_len]) - ord('a')
                if ch.isupper():
                    result.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
                else:
                    result.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
                key_index += 1
            else:
                result.append(ch)

        return ''.join(result)

    def rail_fence_decipher(self, encrypted_text, rails):
        if rails <= 1 or len(encrypted_text) == 0:
            return encrypted_text

        n = len(encrypted_text)
        period = 2 * (rails - 1)

        counts = [0] * rails
        for i in range(n):
            pos = i % period
            if pos < rails:
                rail = pos
            else:
                rail = period - pos
            counts[rail] += 1

        rail_strings = []
        idx = 0
        for count in counts:
            rail_strings.append(encrypted_text[idx:idx + count])
            idx += count

        result = []
        pointers = [0] * rails

        for i in range(n):
            pos = i % period
            if pos < rails:
                rail = pos
            else:
                rail = period - pos
            result.append(rail_strings[rail][pointers[rail]])
            pointers[rail] += 1

        return ''.join(result)

import unittest

class DecryptionUtilsTestVigenereDecipher(unittest.TestCase):
    def test_vigenere_decipher(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.vigenere_decipher('ifmmp'), 'ybocl')

    def test_vigenere_decipher_2(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.vigenere_decipher('rijvs'), 'hello')

    def test_vigenere_decipher_3(self):
        d = DecryptionUtils('longkey')
        self.assertEqual(d.vigenere_decipher('LpPjOjE'), 'AbCdEfG')

    def test_vigenere_decipher_4(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.vigenere_decipher('bcd'), 'ryf')

    def test_vigenere_decipher_5(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.vigenere_decipher('bcdaa'), 'ryfqw')

    def test_vigenere_decipher_6(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.vigenere_decipher('123'), '123')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
