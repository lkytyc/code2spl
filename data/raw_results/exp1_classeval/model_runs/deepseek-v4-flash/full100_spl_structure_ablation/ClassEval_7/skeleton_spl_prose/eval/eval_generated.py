class BalancedBrackets:
    """
    This is a class that checks for bracket matching
    """

    def __init__(self, expr):
        """
        Initializes the class with an expression.
        :param expr: The expression to check for balanced brackets,str.
        """
        self.stack = []
        self.left_brackets = ["(", "{", "["]
        self.right_brackets = [")", "}", "]"]
        self.expr = expr

    def clear_expr(self):
        """
        Clears the expression of all characters that are not brackets.
        >>> b = BalancedBrackets("a(b)c")
        >>> b.clear_expr()
        >>> b.expr
        '()'

        """
        old_expr = self.expr
        kept_chars = [c for c in old_expr if c in self.left_brackets or c in self.right_brackets]
        filtered_expr = ''.join(kept_chars)
        self.expr = filtered_expr

    def check_balanced_brackets(self):
        """
        Checks if the expression has balanced brackets.
        :return: True if the expression has balanced brackets, False otherwise.
        >>> b = BalancedBrackets("a(b)c")
        >>> b.check_balanced_brackets()
        True

        """
        self.clear_expr()
        for Brkt in self.expr:
            is_left_bracket = Brkt in self.left_brackets
            if is_left_bracket:
                self.stack.append(Brkt)
            else:
                if not self.stack:
                    return False
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


class BalancedBracketsTestCheckBalancedBrackets(unittest.TestCase):
    def test_check_balanced_brackets(self):
        b = BalancedBrackets("a(b)c")
        self.assertEqual(b.check_balanced_brackets(), True)

    def test_check_balanced_brackets_2(self):
        b = BalancedBrackets("a(b){c}")
        self.assertEqual(b.check_balanced_brackets(), True)

    def test_check_balanced_brackets_3(self):
        b = BalancedBrackets("[a](b){c}")
        self.assertEqual(b.check_balanced_brackets(), True)

    def test_check_balanced_brackets_4(self):
        b = BalancedBrackets("[a(b){c}")
        self.assertEqual(b.check_balanced_brackets(), False)

    def test_check_balanced_brackets_5(self):
        b = BalancedBrackets("a(b{c}]")
        self.assertEqual(b.check_balanced_brackets(), False)

    def test_check_balanced_brackets_6(self):
        b = BalancedBrackets("a(b{c]]")
        self.assertEqual(b.check_balanced_brackets(), False)

    def test_check_balanced_brackets_7(self):
        b = BalancedBrackets("[a)(b){c}")
        self.assertEqual(b.check_balanced_brackets(), False)


class BalancedBracketsTestMain(unittest.TestCase):
    def test_main(self):
        b = BalancedBrackets("a(b)c")
        b.clear_expr()
        self.assertEqual(b.expr, "()")
        self.assertEqual(b.check_balanced_brackets(), True)

    def test_main_2(self):
        b = BalancedBrackets("[a(b){c}")
        b.clear_expr()
        self.assertEqual(b.expr, "[(){}")
        self.assertEqual(b.check_balanced_brackets(), False)

    def test_main_3(self):
        b = BalancedBrackets("a(b{c}]")
        b.clear_expr()
        self.assertEqual(b.expr, "({}]")
        self.assertEqual(b.check_balanced_brackets(), False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
