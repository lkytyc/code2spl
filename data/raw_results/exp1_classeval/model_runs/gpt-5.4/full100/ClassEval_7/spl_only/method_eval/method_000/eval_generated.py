class BalancedBrackets:
    def __init__(self, expr):
        self.stack = []
        self.left_brackets = ["(", "{", "["]
        self.right_brackets = [")", "}", "]"]
        self.expr = expr

    def clear_expr(self):
        filtered_characters = [
            ch for ch in self.expr
            if ch in self.left_brackets or ch in self.right_brackets
        ]
        filtered_expr = "".join(filtered_characters)
        self.expr = filtered_expr

    def check_balanced_brackets(self):
        self.clear_expr()
        for Brkt in self.expr:
            if Brkt in self.left_brackets:
                self.stack.append(Brkt)
            else:
                Current_Brkt = self.stack.pop()
                if Current_Brkt == "(":
                    if Brkt != ")":
                        return False
                elif Current_Brkt == "{":
                    if Brkt != "}":
                        return False
                elif Current_Brkt == "[":
                    if Brkt != "]":
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
