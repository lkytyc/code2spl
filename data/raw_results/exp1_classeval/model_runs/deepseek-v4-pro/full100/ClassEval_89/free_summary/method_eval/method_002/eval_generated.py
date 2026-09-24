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
