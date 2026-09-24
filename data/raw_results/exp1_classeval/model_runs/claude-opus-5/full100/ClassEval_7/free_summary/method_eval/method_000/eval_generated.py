class BalancedBrackets:
    def __init__(self, expression):
        self.expression = expression
        self.stack = []
        self.opening = ['(', '{', '[']
        self.closing = [')', '}', ']']

    def clear_expr(self):
        self.expression = ''.join(
            ch for ch in self.expression
            if ch in self.opening or ch in self.closing
        )

    def check_balanced_brackets(self):
        self.clear_expr()
        for ch in self.expression:
            if ch in self.opening:
                self.stack.append(ch)
            elif ch in self.closing:
                if not self.stack:
                    return False
                top = self.stack.pop()
                if self.opening.index(top) != self.closing.index(ch):
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
