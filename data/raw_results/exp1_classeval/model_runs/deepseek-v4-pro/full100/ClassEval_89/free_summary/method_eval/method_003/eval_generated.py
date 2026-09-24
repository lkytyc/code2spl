class TwentyFourPointGame:
    def __init__(self):
        self.nums = []

    def _generate_cards(self):
        import random
        self.nums = [random.randint(1, 9) for _ in range(4)]

    def get_my_cards(self):
        self.nums.clear()
        self._generate_cards()
        return self.nums

    def answer(self, expression):
        if expression.lower() == 'pass':
            return self.get_my_cards()
        if not self._validate_expression(expression):
            return False
        return self.evaluate_expression(expression)

    def _validate_expression(self, expression):
        available = list(self.nums)
        for ch in expression:
            if ch.isdigit():
                digit = int(ch)
                if digit in available:
                    available.remove(digit)
                else:
                    return False
        return True

    def evaluate_expression(self, expression):
        try:
            result = eval(expression)
            return result == 24
        except Exception:
            return False

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
