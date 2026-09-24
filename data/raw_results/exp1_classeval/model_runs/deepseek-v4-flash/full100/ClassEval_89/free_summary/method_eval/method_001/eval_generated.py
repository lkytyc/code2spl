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
