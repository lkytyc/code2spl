class ExpressionCalculator:
    def __init__(self):
        self.postfix_stack = []
        self.operat_priority = [0] * 256
        self.operat_priority[ord('+')] = 1
        self.operat_priority[ord('-')] = 1
        self.operat_priority[ord('*')] = 2
        self.operat_priority[ord('/')] = 2
        self.operat_priority[ord('%')] = 2
        self.operat_priority[ord('~')] = 3

    @staticmethod
    def is_operator(c):
        return c in "+-*/%~"

    def compare(self, op1, op2):
        return self.operat_priority[ord(op1)] - self.operat_priority[ord(op2)]

    def transform(self, expression):
        expression = expression.replace(" ", "").rstrip("=")
        if not expression:
            return ""
        if expression[0] == '-':
            expression = "0" + expression
        result = []
        i = 0
        while i < len(expression):
            c = expression[i]
            if c == '-' and (i == 0 or expression[i-1] in "(+-*/%~"):
                result.append('~')
            else:
                result.append(c)
            i += 1
        return "".join(result)

    def prepare(self, expression):
        self.postfix_stack = []
        op_stack = []
        i = 0
        while i < len(expression):
            c = expression[i]
            if c.isdigit() or c == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                self.postfix_stack.append(expression[i:j])
                i = j
            elif c == '(':
                op_stack.append(c)
                i += 1
            elif c == ')':
                while op_stack and op_stack[-1] != '(':
                    self.postfix_stack.append(op_stack.pop())
                if op_stack:
                    op_stack.pop()
                i += 1
            elif self.is_operator(c):
                while op_stack and op_stack[-1] != '(' and self.compare(op_stack[-1], c) >= 0:
                    self.postfix_stack.append(op_stack.pop())
                op_stack.append(c)
                i += 1
            else:
                i += 1
        while op_stack:
            self.postfix_stack.append(op_stack.pop())

    @staticmethod
    def _calculate(op, left, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '%':
            return left % right
        elif op == '~':
            return -right
        else:
            raise ValueError("Unknown operator: " + op)

    def calculate(self, expression):
        transformed = self.transform(expression)
        self.prepare(transformed)
        result_stack = []
        for token in self.postfix_stack:
            if token in "+-*/%~":
                if token == '~':
                    right = result_stack.pop()
                    result_stack.append(self._calculate(token, None, right))
                else:
                    right = result_stack.pop()
                    left = result_stack.pop()
                    result_stack.append(self._calculate(token, left, right))
            else:
                result_stack.append(Decimal(token))
        return float(result_stack[0]) if result_stack else 0.0

import unittest

class ExpressionCalculatorTestCompare(unittest.TestCase):
    def setUp(self):
        self.expression_calculator = ExpressionCalculator()

    def test_compare_1(self):
        result = self.expression_calculator.compare("+", "-")
        self.assertTrue(result)

    def test_compare_2(self):
        result = self.expression_calculator.compare("*", "/")
        self.assertTrue(result)

    def test_compare_3(self):
        result = self.expression_calculator.compare("+", "*")
        self.assertTrue(result)

    def test_compare_4(self):
        result = self.expression_calculator.compare("*", "+")
        self.assertFalse(result)

    def test_compare_5(self):
        result = self.expression_calculator.compare("/", "+")
        self.assertFalse(result)

    def test_compare_6(self):
        result = self.expression_calculator.compare("%", "+")
        self.assertFalse(result)

    def test_compare_7(self):
        result = self.expression_calculator.compare("+", "%")
        self.assertTrue(result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
