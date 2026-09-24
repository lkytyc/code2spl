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
        shift %= 26
        for ch in ciphertext:
            if 'a' <= ch <= 'z':
                result.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
            elif 'A' <= ch <= 'Z':
                result.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(ch)
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

        for ch in ciphertext:
            if ch.isalpha():
                k = key[key_index % len(key)]
                if k.isalpha():
                    shift = ord(k.lower()) - ord('a')
                else:
                    shift = 0

                if 'a' <= ch <= 'z':
                    result.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
                else:
                    result.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
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
        >>> d = DecryptionUtils('key')
        >>> d.rail_fence_decipher('Hoo!el,Wrdl l', 3)
        'Hello, World!'

        """
        if rails <= 1 or not encrypted_text:
            return encrypted_text

        n = len(encrypted_text)
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

        counts = [0] * rails
        for r in pattern:
            counts[r] += 1

        rails_text = []
        idx = 0
        for c in counts:
            rails_text.append(list(encrypted_text[idx:idx + c]))
            idx += c

        positions = [0] * rails
        plaintext = []
        for r in pattern:
            plaintext.append(rails_text[r][positions[r]])
            positions[r] += 1

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


class DecryptionUtilsTestMain(unittest.TestCase):
    def test_main(self):
        d = DecryptionUtils('key')
        self.assertEqual(d.caesar_decipher('ifmmp', 1), 'hello')
        self.assertEqual(d.vigenere_decipher('ifmmp'), 'ybocl')
        self.assertEqual(d.rail_fence_decipher('Hoo!el,Wrdl l', 3), 'Hello, World!')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
