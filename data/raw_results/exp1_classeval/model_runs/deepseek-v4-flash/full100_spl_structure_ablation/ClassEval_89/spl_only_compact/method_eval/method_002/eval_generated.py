import random

class TwentyFourPointGame:
    def __init__(self):
        self.nums = []

    def _generate_cards(self):
        for i in range(4):
            self.nums.append(random.randint(1, 9))
        assert len(self.nums) == 4, "Assertion failed: len(self.nums) == 4"

    def answer(self, expression: str):
        if expression == 'pass':
            return self.get_my_cards()
        statistic = {}
        for c in expression:
            if c.isdigit() and int(c) in self.nums:
                statistic[c] = statistic.get(c, 0) + 1
        nums_used = statistic.copy()
        for num in self.nums:
            if nums_used.get(str(num), -100) != -100 and nums_used[str(num)] > 0:
                nums_used[str(num)] -= 1
            else:
                return False
        if all(count == 0 for count in nums_used.values()):
            return self.evaluate_expression(expression)
        else:
            return False

    def evaluate_expression(self, expression: str) -> bool:
        try:
            evaluated_value = eval(expression)
            comparison_result = evaluated_value == 24
            if comparison_result:
                return True
            else:
                return False
        except Exception:
            return False

    def get_my_cards(self) -> list:
        self.nums = []
        self._generate_cards()
        return self.nums

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
