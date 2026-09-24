class BalancedBrackets:
    def __init__(self, expr: str):
        self.stack = []
        self.left_brackets = ['(', '{', '[']
        self.right_brackets = [')', '}', ']']
        self.expr = expr

    def check_balanced_brackets(self) -> bool:
        self.clear_expr()
        self.stack = []

        for Brkt in self.expr:
            if Brkt in self.left_brackets:
                self.stack.append(Brkt)
            else:
                if not self.stack:
                    return False
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

    def clear_expr(self):
        self.expr = "".join(
            c for c in self.expr
            if c in self.left_brackets or c in self.right_brackets
        )

import unittest

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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
