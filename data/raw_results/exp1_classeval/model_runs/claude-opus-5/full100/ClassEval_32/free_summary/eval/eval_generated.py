class DecryptionUtils:
    def __init__(self, key: str):
        self.key = key.upper()

    def caesar_decipher(self, ciphertext: str, shift: int) -> str:
        result = []
        for ch in ciphertext:
            if ch.isalpha():
                base = ord('A') if ch.isupper() else ord('a')
                result.append(chr((ord(ch) - base - shift) % 26 + base))
            else:
                result.append(ch)
        return ''.join(result)

    def vigenere_decipher(self, ciphertext: str) -> str:
        result = []
        key_index = 0
        for ch in ciphertext:
            if ch.isalpha():
                key_shift = ord(self.key[key_index % len(self.key)]) - ord('A')
                base = ord('A') if ch.isupper() else ord('a')
                result.append(chr((ord(ch) - base - key_shift) % 26 + base))
                key_index += 1
            else:
                result.append(ch)
        return ''.join(result)

    def rail_fence_decipher(self, encrypted_text: str, rails: int) -> str:
        n = len(encrypted_text)
        if rails == 1 or rails >= n:
            return encrypted_text

        # First pass: determine which rail each position belongs to
        # and count how many characters go on each rail
        pattern = []
        rail = 0
        direction = 1
        for i in range(n):
            pattern.append(rail)
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
            rail += direction

        # Count characters per rail
        rail_lengths = [0] * rails
        for r in pattern:
            rail_lengths[r] += 1

        # Slice the encrypted text into rails
        rail_strings = []
        idx = 0
        for length in rail_lengths:
            rail_strings.append(list(encrypted_text[idx:idx + length]))
            idx += length

        # Second pass: read back along the zigzag pattern
        rail_indices = [0] * rails
        result = []
        for r in pattern:
            result.append(rail_strings[r][rail_indices[r]])
            rail_indices[r] += 1

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
