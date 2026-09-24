import random


class TwentyFourPointGame:
    def __init__(self):
        self.nums = []

    def _generate_cards(self):
        self.nums = [random.randint(1, 9) for _ in range(4)]

    def get_my_cards(self):
        self.nums = []
        self._generate_cards()
        return self.nums

    def answer(self, expression):
        if expression == 'pass':
            return self.get_my_cards()

        # Count digits in the expression and compare against hand
        hand = list(self.nums)
        for char in expression:
            if char.isdigit() and char != '0':
                digit = int(char)
                if digit in hand:
                    hand.remove(digit)
                else:
                    return False

        if hand:
            return False

        return self.evaluate_expression(expression)

    def evaluate_expression(self, expression):
        try:
            result = eval(expression)
            return result == 24
        except Exception:
            return False

import unittest

class TwentyFourPointGameTestEvaluateExpression(unittest.TestCase):
    def test_evaluate_expression_1(self):
        game = TwentyFourPointGame()
        result = game.evaluate_expression('4+3+6+6')
        self.assertFalse(result)

    def test_evaluate_expression_2(self):
        game = TwentyFourPointGame()
        result = game.evaluate_expression('4*3+6+6')
        self.assertTrue(result)

    def test_evaluate_expression_3(self):
        game = TwentyFourPointGame()
        result = game.evaluate_expression('1+1+1+1')
        self.assertFalse(result)

    def test_evaluate_expression_4(self):
        game = TwentyFourPointGame()
        result = game.evaluate_expression('1+')
        self.assertFalse(result)

    def test_evaluate_expression_5(self):
        game = TwentyFourPointGame()
        result = game.evaluate_expression('abc')
        self.assertFalse(result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
