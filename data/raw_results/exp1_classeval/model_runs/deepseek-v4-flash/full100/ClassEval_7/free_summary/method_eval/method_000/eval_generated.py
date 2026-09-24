class BalancedBrackets:
    def __init__(self, expression):
        self.expr = expression
        self.stack = []
        self.left_brackets = ['(', '[', '{']
        self.right_brackets = [')', ']', '}']

    def clear_expr(self):
        self.expr = ''.join(
            ch for ch in self.expr
            if ch in self.left_brackets or ch in self.right_brackets
        )

    def check_balanced_brackets(self):
        self.clear_expr()
        self.stack.clear()

        for char in self.expr:
            if char in self.left_brackets:
                self.stack.append(char)
            elif char in self.right_brackets:
                if not self.stack:
                    return False
                expected_left = self.left_brackets[self.right_brackets.index(char)]
                if self.stack.pop() != expected_left:
                    return False

        return len(self.stack) == 0

import unittest

class BalancedBracketsTestClearExpr(unittest.TestCase):
    def test_clear_expr(self):
        b = BalancedBrackets("a(b)c")
        b.clear_expr()
        self.assertEqual(b.expr, "()")

    def test_clear_expr_2(self):
        b = BalancedBrackets("a(b){c}")
        b.clear_expr()
        self.assertEqual(b.expr, "(){}")

    def test_clear_expr_3(self):
        b = BalancedBrackets("[a](b){c}")
        b.clear_expr()
        self.assertEqual(b.expr, "[](){}")

    def test_clear_expr_4(self):
        b = BalancedBrackets("[a(b){c}")
        b.clear_expr()
        self.assertEqual(b.expr, "[(){}")

    def test_clear_expr_5(self):
        b = BalancedBrackets("a(b){c}]")
        b.clear_expr()
        self.assertEqual(b.expr, "(){}]")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
