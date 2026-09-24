class DecryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_decipher(self, ciphertext, shift):
        plaintext = []
        shift = shift % 26
        for ch in ciphertext:
            if 'A' <= ch <= 'Z':
                plaintext.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
            elif 'a' <= ch <= 'z':
                plaintext.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
            else:
                plaintext.append(ch)
        return ''.join(plaintext)

    def vigenere_decipher(self, ciphertext):
        if not self.key:
            return ciphertext

        plaintext = []
        key_letters = [ch for ch in self.key if ch.isalpha()]
        if not key_letters:
            return ciphertext

        key_index = 0
        key_len = len(key_letters)

        for ch in ciphertext:
            if ch.isalpha():
                k = key_letters[key_index % key_len]
                shift = ord(k.lower()) - ord('a')
                if 'A' <= ch <= 'Z':
                    plaintext.append(chr((ord(ch) - ord('A') - shift) % 26 + ord('A')))
                else:
                    plaintext.append(chr((ord(ch) - ord('a') - shift) % 26 + ord('a')))
                key_index += 1
            else:
                plaintext.append(ch)
        return ''.join(plaintext)

    def rail_fence_decipher(self, encrypted_text, rails):
        if rails <= 1 or len(encrypted_text) <= 1:
            return encrypted_text

        n = len(encrypted_text)
        pattern = []
        rail = 0
        direction = 1
        for _ in range(n):
            pattern.append(rail)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction

        rail_counts = [0] * rails
        for r in pattern:
            rail_counts[r] += 1

        rails_text = []
        idx = 0
        for count in rail_counts:
            rails_text.append(list(encrypted_text[idx:idx + count]))
            idx += count

        positions = [0] * rails
        result = []
        for r in pattern:
            result.append(rails_text[r][positions[r]])
            positions[r] += 1

        return ''.join(result)

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
