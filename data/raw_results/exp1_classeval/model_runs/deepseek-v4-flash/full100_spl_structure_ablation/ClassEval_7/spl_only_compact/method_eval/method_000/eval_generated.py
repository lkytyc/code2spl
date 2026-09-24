class BalancedBrackets:
    def __init__(self, expr: str):
        self.stack = []
        self.left_brackets = ['(', '{', '[']
        self.right_brackets = [')', '}', ']']
        self.expr = expr

    def check_balanced_brackets(self) -> bool:
        self.clear_expr()
        for Brkt in self.expr:
            is_left_bracket = Brkt in self.left_brackets
            if is_left_bracket:
                self.stack.append(Brkt)
            else:
                Current_Brkt = self.stack.pop()
                if Current_Brkt == '(' and Brkt != ')':
                    return False
                if Current_Brkt == '{' and Brkt != '}':
                    return False
                if Current_Brkt == '[' and Brkt != ']':
                    return False
        if self.stack:
            return False
        return True

    def clear_expr(self):
        old_expr = self.expr
        kept_chars = [c for c in old_expr if c in self.left_brackets or c in self.right_brackets]
        filtered_expr = ''.join(kept_chars)
        self.expr = filtered_expr

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
