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
        """
        result = []
        for ch in ciphertext:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                result.append(chr((ord(ch) - base - shift) % 26 + base))
            else:
                result.append(ch)
        return ''.join(result)

    def vigenere_decipher(self, ciphertext):
        """
        Deciphers the given ciphertext using the Vigenere cipher
        :param ciphertext: The ciphertext to decipher,str.
        :return: The deciphered plaintext,str.
        """
        key_shifts = [(ord(c.lower()) - ord('a')) % 26 for c in self.key if c.isalpha()]
        if not key_shifts:
            key_shifts = [0]

        result = []
        key_index = 0

        for ch in ciphertext:
            if ch.isalpha():
                shift = key_shifts[key_index % len(key_shifts)]
                base = ord('A') if ch.isupper() else ord('a')
                result.append(chr((ord(ch) - base - shift) % 26 + base))
                key_index += 1
            else:
                result.append(ch)

        return ''.join(result)

    def rail_fence_decipher(self, encrypted_text, rails):
        """
        Deciphers the given ciphertext using the Rail Fence cipher
        :param encrypted_text: The ciphertext to decipher,str.
        :param rails: The number of rails to use for decryption,int.
        :return: The deciphered plaintext,str.
        """
        if rails <= 1:
            return encrypted_text

        n = len(encrypted_text)
        cycle_len = 2 * rails - 2
        positions = [[] for _ in range(rails)]

        for i in range(n):
            pos_in_cycle = i % cycle_len
            if pos_in_cycle < rails:
                rail = pos_in_cycle
            else:
                rail = cycle_len - pos_in_cycle
            positions[rail].append(i)

        plaintext = [''] * n
        idx = 0

        for rail in range(rails):
            for pos in positions[rail]:
                plaintext[pos] = encrypted_text[idx]
                idx += 1

        return ''.join(plaintext)

import unittest

class DecryptionUtilsTestCaesarDecipher(unittest.TestCase):
    def test_caesar_decipher(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.caesar_decipher('ifmmp', 1), 'hello')

    def test_caesar_decipher_2(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.caesar_decipher('bcdyza', 27), 'abcxyz')

    def test_caesar_decipher_3(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.caesar_decipher('bcd', 0), 'bcd')

    def test_caesar_decipher_4(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.caesar_decipher('bcd', 26), 'bcd')

    def test_caesar_decipher_5(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.caesar_decipher('bcd', -26), 'bcd')

    def test_caesar_decipher_6(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.caesar_decipher('IFMMP', 1), 'HELLO')

    def test_caesar_decipher_7(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.caesar_decipher('123', 1), '123')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
