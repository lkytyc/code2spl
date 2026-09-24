class TwentyFourPointGame:
    def __init__(self):
        self.nums = []

    def _generate_cards(self):
        import random
        for _ in range(4):
            self.nums.append(random.randint(1, 9))

    def get_my_cards(self):
        self.nums = []
        self._generate_cards()
        return self.nums

    def evaluate_expression(self, expression):
        try:
            return eval(expression) == 24
        except Exception:
            return False

    def answer(self, expression):
        if expression == 'pass':
            return self.get_my_cards()

        if not self.nums:
            return False

        card_counts = {}
        for n in self.nums:
            card_counts[n] = card_counts.get(n, 0) + 1

        expr_counts = {}
        current_digit = ''
        for ch in expression:
            if ch.isdigit():
                current_digit += ch
            else:
                if current_digit:
                    value = int(current_digit)
                    expr_counts[value] = expr_counts.get(value, 0) + 1
                    current_digit = ''
        if current_digit:
            value = int(current_digit)
            expr_counts[value] = expr_counts.get(value, 0) + 1

        for value, count in expr_counts.items():
            if card_counts.get(value, 0) < count:
                return False

        return self.evaluate_expression(expression)

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
