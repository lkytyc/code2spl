class DecryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_decipher(self, ciphertext, shift):
        plaintext = ""
        for char in ciphertext:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                shifted_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
                plaintext += shifted_char
            else:
                plaintext += char
        return plaintext

    def vigenere_decipher(self, ciphertext):
        decrypted_text = ""
        key_index = 0
        for char in ciphertext:
            if char.isalpha():
                shift = ord(self.key[key_index % len(self.key)].lower()) - ord('a')
                decrypted_char = chr((ord(char.lower()) - ord('a') - shift) % 26 + ord('a'))
                if char.isupper():
                    decrypted_text += decrypted_char.upper()
                else:
                    decrypted_text += decrypted_char
                key_index += 1
            else:
                decrypted_text += char
        return decrypted_text

    def rail_fence_decipher(self, encrypted_text, rails):
        fence = [['\n'] * len(encrypted_text) for _ in range(rails)]
        direction = -1
        row = 0
        col = 0

        for _ in range(len(encrypted_text)):
            if row == 0 or row == rails - 1:
                direction = -direction
            fence[row][col] = ''
            col += 1
            row += direction

        index = 0
        for i in range(rails):
            for j in range(len(encrypted_text)):
                if fence[i][j] == '':
                    fence[i][j] = encrypted_text[index]
                    index += 1

        plain_text = ""
        direction = -1
        row = 0
        col = 0

        for _ in range(len(encrypted_text)):
            if row == 0 or row == rails - 1:
                direction = -direction
            plain_text += fence[row][col]
            col += 1
            row += direction

        return plain_text

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
