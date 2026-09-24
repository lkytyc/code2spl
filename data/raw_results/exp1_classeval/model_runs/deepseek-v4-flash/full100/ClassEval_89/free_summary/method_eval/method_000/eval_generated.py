import random
import re

class Game24:
    def __init__(self):
        self.cards = []
        self.get_my_cards()

    def get_my_cards(self):
        self.cards = [random.randint(1, 9) for _ in range(4)]
        return self.cards

    def answer(self, expression):
        if expression == 'pass':
            return self.get_my_cards()

        # Extract all digits from the expression
        digits_in_expr = re.findall(r'\d', expression)
        if len(digits_in_expr) != 4:
            return False

        # Check that each digit in expression is from the current cards and used exactly once
        cards_copy = self.cards[:]
        for d in digits_in_expr:
            num = int(d)
            if num in cards_copy:
                cards_copy.remove(num)
            else:
                return False

        # Evaluate the expression
        try:
            result = eval(expression)
            return abs(result - 24) < 1e-9
        except:
            return False

import unittest

class TwentyFourPointGameTestGetMyCards(unittest.TestCase):
    def test_get_my_cards_1(self):
        game = TwentyFourPointGame()
        cards = game.get_my_cards()
        self.assertEqual(len(cards), 4)
        for card in cards:
            self.assertIn(card, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_get_my_cards_2(self):
        game = TwentyFourPointGame()
        cards = game.get_my_cards()
        self.assertEqual(len(cards), 4)
        for card in cards:
            self.assertIn(card, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_get_my_cards_3(self):
        game = TwentyFourPointGame()
        cards = game.get_my_cards()
        self.assertEqual(len(cards), 4)
        for card in cards:
            self.assertIn(card, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_get_my_cards_4(self):
        game = TwentyFourPointGame()
        cards = game.get_my_cards()
        self.assertEqual(len(cards), 4)
        for card in cards:
            self.assertIn(card, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_get_my_cards_5(self):
        game = TwentyFourPointGame()
        cards = game.get_my_cards()
        self.assertEqual(len(cards), 4)
        for card in cards:
            self.assertIn(card, [1, 2, 3, 4, 5, 6, 7, 8, 9])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
