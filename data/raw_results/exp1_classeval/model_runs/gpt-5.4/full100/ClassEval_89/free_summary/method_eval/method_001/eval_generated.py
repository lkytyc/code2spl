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

class TwentyFourPointGameTestAnswer(unittest.TestCase):
    def test_answer_1(self):
        game = TwentyFourPointGame()
        cards = game.answer('pass')
        self.assertEqual(len(cards), 4)

    def test_answer_2(self):
        game = TwentyFourPointGame()
        result = game.answer('4*3+6+6')
        self.assertTrue(result)

    def test_answer_3(self):
        game = TwentyFourPointGame()
        result = game.answer('1+1+1+1')
        self.assertFalse(result)

    def test_answer_4(self):
        game = TwentyFourPointGame()
        result = game.answer('1+')
        self.assertFalse(result)

    def test_answer_5(self):
        game = TwentyFourPointGame()
        result = game.answer('abc')
        self.assertFalse(result)

    def test_answer_6(self):
        game = TwentyFourPointGame()
        game.nums = [1, 1, 1, 1]
        result = game.answer('1+1+1+2')
        self.assertFalse(result)

    def test_answer_7(self):
        game = TwentyFourPointGame()
        game.nums = [1, 1, 1, 1]
        result = game.answer('1+1+1+1+1')
        self.assertFalse(result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
