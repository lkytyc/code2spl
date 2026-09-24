import random

class TwentyFourPointGame:
    def __init__(self):
        self.nums = []
        self._generate_cards()

    def _generate_cards(self):
        self.nums = [random.randint(1, 9) for _ in range(4)]
        return self.nums

    def get_my_cards(self):
        self.nums = []
        return self._generate_cards()

    def evaluate_expression(self, expression):
        try:
            return eval(expression) == 24
        except Exception:
            return False

    def answer(self, expression):
        if expression == 'pass':
            return self.get_my_cards()

        counts = {}
        for c in expression:
            if c.isdigit():
                n = int(c)
                if n in self.nums:
                    counts[n] = counts.get(n, 0) + 1

        required = {}
        for n in self.nums:
            required[n] = required.get(n, 0) + 1

        if counts != required:
            return False

        return self.evaluate_expression(expression)

import unittest

class TwentyFourPointGameTest(unittest.TestCase):
    def test_TwentyFourPointGame(self):
        game = TwentyFourPointGame()
        cards = game.get_my_cards()
        self.assertEqual(len(cards), 4)
        for card in cards:
            self.assertIn(card, [1, 2, 3, 4, 5, 6, 7, 8, 9])
        game.nums = [4, 3, 6, 6]
        result = game.answer('4*3+6+6')
        self.assertTrue(result)
        result = game.evaluate_expression('4*3+6+6')
        self.assertTrue(result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
