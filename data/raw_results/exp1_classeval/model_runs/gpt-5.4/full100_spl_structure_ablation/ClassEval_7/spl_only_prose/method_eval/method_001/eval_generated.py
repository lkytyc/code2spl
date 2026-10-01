class BalancedBrackets:
    def __init__(self, expr: str):
        self.stack = []
        self.left_brackets = ["(", "{", "["]
        self.right_brackets = [")", "}", "]"]
        self.expr = expr

    def check_balanced_brackets(self) -> bool:
        self.clear_expr()

        for Brkt in self.expr:
            if Brkt in self.left_brackets:
                self.stack.append(Brkt)
            else:
                Current_Brkt = self.stack.pop()

                if Current_Brkt == "(" and Brkt != ")":
                    return False
                if Current_Brkt == "{" and Brkt != "}":
                    return False
                if Current_Brkt == "[" and Brkt != "]":
                    return False

        if self.stack:
            return False

        return True

    def clear_expr(self):
        filtered_characters = [
            character
            for character in self.expr
            if character in self.left_brackets or character in self.right_brackets
        ]
        filtered_expr = "".join(filtered_characters)
        self.expr = filtered_expr

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
