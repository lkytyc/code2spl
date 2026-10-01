class DecryptionUtils:
    def __init__(self, key: any):
        self.key = key

    def caesar_decipher(self, ciphertext: str, shift: int) -> str:
        plaintext = ""
        for char in ciphertext:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                shifted_char = chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
                plaintext += shifted_char
            else:
                plaintext += char
        return plaintext

    def rail_fence_decipher(self, encrypted_text: str, rails: int) -> str:
        fence = [["\n" for _ in range(len(encrypted_text))] for _ in range(rails)]
        direction = -1
        row = 0
        col = 0

        for _ in range(len(encrypted_text)):
            if row == 0 or row == rails - 1:
                direction *= -1
            fence[row][col] = ""
            col += 1
            row += direction

        index = 0
        for i in range(rails):
            for j in range(len(encrypted_text)):
                if fence[i][j] == "":
                    fence[i][j] = encrypted_text[index]
                    index += 1

        plain_text = ""
        direction = -1
        row = 0
        col = 0
        for _ in range(len(encrypted_text)):
            if row == 0 or row == rails - 1:
                direction *= -1
            plain_text += fence[row][col]
            col += 1
            row += direction

        return plain_text

    def vigenere_decipher(ciphertext: str) -> str:
        decrypted_text = ""
        key_index = 0
        for char in ciphertext:
            if char.isalpha():
                shift = ord(self.key[key_index % len(self.key)].lower()) - ord("a")
                decrypted_char = chr((ord(char.lower()) - ord("a") - shift) % 26 + ord("a"))
                if char.isupper():
                    decrypted_char = decrypted_char.upper()
                decrypted_text += decrypted_char
                key_index += 1
            else:
                decrypted_text += char
        return decrypted_text

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
