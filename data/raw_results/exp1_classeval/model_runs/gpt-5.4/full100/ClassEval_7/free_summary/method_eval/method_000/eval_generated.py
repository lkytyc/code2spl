class BalancedBrackets:
    def __init__(self, expr):
        self.expr = expr
        self.stack = []
        self.opening_brackets = ['(', '{', '[']
        self.closing_brackets = [')', '}', ']']

    def clear_expr(self):
        self.expr = ''.join(
            ch for ch in self.expr
            if ch in self.opening_brackets or ch in self.closing_brackets
        )

    def check_balanced_brackets(self):
        self.clear_expr()
        self.stack = []

        for ch in self.expr:
            if ch in self.opening_brackets:
                self.stack.append(ch)
            elif ch in self.closing_brackets:
                opening = self.stack.pop()
                if (
                    (opening == '(' and ch != ')') or
                    (opening == '{' and ch != '}') or
                    (opening == '[' and ch != ']')
                ):
                    return False

        if self.stack:
            return False

        return True

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
