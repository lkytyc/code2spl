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
        result = []
        shift = shift % 26

        for char in ciphertext:
            if 'a' <= char <= 'z':
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(char)

        return ''.join(result)

    def vigenere_decipher(self, ciphertext):
        """
        Deciphers the given ciphertext using the Vigenere cipher
        :param ciphertext: The ciphertext to decipher,str.
        :return: The deciphered plaintext,str.
        >>> d = DecryptionUtils('key')
        >>> d.vigenere_decipher('ifmmp')
        'ybocl'

        """
        if not self.key:
            return ciphertext

        result = []
        key = self.key
        key_index = 0
        key_len = len(key)

        for char in ciphertext:
            if 'a' <= char <= 'z':
                key_char = key[key_index % key_len].lower()
                shift = ord(key_char) - ord('a')
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
                key_index += 1
            elif 'A' <= char <= 'Z':
                key_char = key[key_index % key_len].lower()
                shift = ord(key_char) - ord('a')
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
                key_index += 1
            else:
                result.append(char)

        return ''.join(result)

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
        if rails <= 1 or rails >= len(encrypted_text):
            return encrypted_text

        n = len(encrypted_text)
        pattern = []
        row = 0
        direction = 1

        for _ in range(n):
            pattern.append(row)
            if row == 0:
                direction = 1
            elif row == rails - 1:
                direction = -1
            row += direction

        rail_counts = [0] * rails
        for r in pattern:
            rail_counts[r] += 1

        rails_chars = []
        index = 0
        for count in rail_counts:
            rails_chars.append(list(encrypted_text[index:index + count]))
            index += count

        rail_positions = [0] * rails
        result = []

        for r in pattern:
            result.append(rails_chars[r][rail_positions[r]])
            rail_positions[r] += 1

        return ''.join(result)

import unittest

class DecryptionUtilsTestRailFenceDecipher(unittest.TestCase):
    def test_rail_fence_decipher(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.rail_fence_decipher('Hoo!el,Wrdl l', 3), 'Hello, World!')

    def test_rail_fence_decipher_2(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.rail_fence_decipher('Hoo!el,Wrdl l', 4), 'H!W reoldll,o')

    def test_rail_fence_decipher_3(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.rail_fence_decipher('Hoo!el,Wrdl l', 5), 'Holr d,!oeWll')

    def test_rail_fence_decipher_4(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.rail_fence_decipher('Hoo!el,Wrdl l', 6), 'Holrll d,!oeW')

    def test_rail_fence_decipher_5(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.rail_fence_decipher('Hoo!el,Wrdl l', 7), 'Hoe,rll dWl!o')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
