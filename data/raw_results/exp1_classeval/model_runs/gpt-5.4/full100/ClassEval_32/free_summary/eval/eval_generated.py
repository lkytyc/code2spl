class DecryptionUtils:
    def __init__(self, key):
        self.key = key

    def caesar_decipher(self, ciphertext, shift):
        result = []
        for char in ciphertext:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                decoded_char = chr((ord(char) - base - shift) % 26 + base)
                result.append(decoded_char)
            else:
                result.append(char)
        return ''.join(result)

    def vigenere_decipher(self, ciphertext):
        if not self.key:
            return ciphertext

        result = []
        key = self.key
        key_index = 0

        for char in ciphertext:
            if char.isalpha():
                key_char = key[key_index % len(key)]
                if key_char.isalpha():
                    shift = ord(key_char.lower()) - ord('a')
                else:
                    shift = 0
                base = ord('A') if char.isupper() else ord('a')
                decoded_char = chr((ord(char) - base - shift) % 26 + base)
                result.append(decoded_char)
                key_index += 1
            else:
                result.append(char)

        return ''.join(result)

    def rail_fence_decipher(self, encrypted_text, rails):
        if rails <= 1 or rails >= len(encrypted_text):
            return encrypted_text

        length = len(encrypted_text)
        grid = [['\n' for _ in range(length)] for _ in range(rails)]

        row, col = 0, 0
        direction_down = None

        for _ in range(length):
            if row == 0:
                direction_down = True
            if row == rails - 1:
                direction_down = False

            grid[row][col] = '*'
            col += 1
            row += 1 if direction_down else -1

        index = 0
        for i in range(rails):
            for j in range(length):
                if grid[i][j] == '*' and index < length:
                    grid[i][j] = encrypted_text[index]
                    index += 1

        result = []
        row, col = 0, 0
        direction_down = None

        for _ in range(length):
            if row == 0:
                direction_down = True
            if row == rails - 1:
                direction_down = False

            if grid[row][col] != '\n':
                result.append(grid[row][col])
                col += 1

            row += 1 if direction_down else -1

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
