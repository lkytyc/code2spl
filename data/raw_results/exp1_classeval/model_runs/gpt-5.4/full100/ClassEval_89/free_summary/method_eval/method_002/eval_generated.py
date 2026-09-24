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
