class DecryptionUtils:
    """
    This is a class that provides methods for decryption, including the Caesar cipher, Vigenere cipher, and Rail Fence cipher.
    """

    def __init__(self, key):
        """
        Initializes the decryption utility with a key.
        :param key: The key to use for decryption,str.
        """
        self.key = key

    def caesar_decipher(self, ciphertext, shift):
        """
        Deciphers the given ciphertext using the Caesar cipher
        :param ciphertext: The ciphertext to decipher,str.
        :param shift: The shift to use for decryption,int.
        :return: The deciphered plaintext,str.
        >>> d = DecryptionUtils('key')
        >>> d.caesar_decipher('ifmmp', 1)
        'hello'

        """
        plaintext = []
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                decrypted = chr((ord(char) - base - shift) % 26 + base)
                plaintext.append(decrypted)
            else:
                plaintext.append(char)
        return ''.join(plaintext)

    def vigenere_decipher(self, ciphertext):
        """
        Deciphers the given ciphertext using the Vigenere cipher
        :param ciphertext: The ciphertext to decipher,str.
        :return: The deciphered plaintext,str.
        >>> d = DecryptionUtils('key')
        >>> d.vigenere_decipher('ifmmp')
        'ybocl'

        """
        plaintext = []
        key_index = 0
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                key_char = self.key[key_index % len(self.key)]
                key_shift = ord(key_char.lower()) - ord('a')
                decrypted = chr((ord(char) - base - key_shift) % 26 + base)
                plaintext.append(decrypted)
                key_index += 1
            else:
                plaintext.append(char)
        return ''.join(plaintext)

    def rail_fence_decipher(self, encrypted_text, rails):
        """
        Deciphers the given ciphertext using the Rail Fence cipher
        :param encrypted_text: The ciphertext to decipher,str.
        :param rails: The number of rails to use for decryption,int.
        :return: The deciphered plaintext,str.
        >>> d = DecryptionUtils('key')
        >>> d.rail_fence_decipher('Hoo!el,Wrdl l', 3)
        'Hello, World!'

        """
        n = len(encrypted_text)
        # Build the zigzag pattern to determine rail assignments
        pattern = [0] * n
        rail = 0
        direction = 1
        for i in range(n):
            pattern[i] = rail
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction

        # Count characters per rail
        rail_lengths = [0] * rails
        for r in pattern:
            rail_lengths[r] += 1

        # Split encrypted text into rail segments
        segments = []
        idx = 0
        for r in range(rails):
            segments.append(list(encrypted_text[idx:idx + rail_lengths[r]]))
            idx += rail_lengths[r]

        # Read off characters in zigzag order
        rail_indices = [0] * rails
        result = []
        for r in pattern:
            result.append(segments[r][rail_indices[r]])
            rail_indices[r] += 1

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
