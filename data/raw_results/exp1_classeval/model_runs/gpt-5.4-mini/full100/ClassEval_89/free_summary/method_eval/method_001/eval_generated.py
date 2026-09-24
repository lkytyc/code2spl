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
