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
