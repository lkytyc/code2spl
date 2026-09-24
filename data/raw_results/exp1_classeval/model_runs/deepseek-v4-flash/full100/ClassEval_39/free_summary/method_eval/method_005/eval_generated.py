class ExpressionCalculator:
    def __init__(self):
        self.operators = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
        self.placeholder = 'u'

    def calculate(self, expression):
        expression = expression.replace(' ', '')
        if expression.endswith('='):
            expression = expression[:-1]
        expression = self._rewrite_unary_minus(expression)
        postfix = self._infix_to_postfix(expression)
        return float(self._evaluate_postfix(postfix))

    def _rewrite_unary_minus(self, expr):
        result = []
        for i, ch in enumerate(expr):
            if ch == '-':
                if i == 0 or expr[i-1] in '+-*/%(':
                    result.append(self.placeholder)
                else:
                    result.append(ch)
            else:
                result.append(ch)
        return ''.join(result)

    def _infix_to_postfix(self, expr):
        output = []
        stack = []
        i = 0
        while i < len(expr):
            ch = expr[i]
            if ch.isdigit() or ch == '.':
                num = ''
                while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                    num += expr[i]
                    i += 1
                output.append(num)
                continue
            elif ch == self.placeholder:
                output.append(ch)
                i += 1
                continue
            elif ch in self.operators:
                while (stack and stack[-1] != '(' and
                       self.operators.get(stack[-1], 0) >= self.operators[ch]):
                    output.append(stack.pop())
                stack.append(ch)
                i += 1
            elif ch == '(':
                stack.append(ch)
                i += 1
            elif ch == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()
                i += 1
            else:
                i += 1
        while stack:
            output.append(stack.pop())
        return output

    def _evaluate_postfix(self, tokens):
        stack = []
        for token in tokens:
            if token == self.placeholder:
                if not stack:
                    raise ValueError("Invalid expression")
                operand = stack.pop()
                stack.append(-operand)
            elif token in self.operators:
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(a, b, token)
                stack.append(result)
            else:
                stack.append(Decimal(token))
        if len(stack) != 1:
            raise ValueError("Invalid expression")
        return stack[0]

    def _apply_operator(self, a, b, op):
        from decimal import Decimal
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b
        elif op == '%':
            if b == 0:
                raise ZeroDivisionError("Modulo by zero")
            return a % b
        else:
            raise ValueError(f"Unknown operator: {op}")

import unittest

class ExpressionCalculatorTestTransform(unittest.TestCase):
    def setUp(self):
        self.expression_calculator = ExpressionCalculator()

    def test_transform_1(self):
        result = self.expression_calculator.transform("2 + 3 * 4")
        self.assertEqual(result, "2+3*4")

    def test_transform_2(self):
        result = self.expression_calculator.transform("2 + 3 / 4")
        self.assertEqual(result, "2+3/4")

    def test_transform_3(self):
        result = self.expression_calculator.transform("2 - 3 * 4")
        self.assertEqual(result, "2-3*4")

    def test_transform_4(self):
        result = self.expression_calculator.transform("1 + 3 * 4")
        self.assertEqual(result, "1+3*4")

    def test_transform_5(self):
        result = self.expression_calculator.transform("-2 + (-3) * 4")
        self.assertEqual(result, "~2+(~3)*4")

    def test_transform_6(self):
        result = self.expression_calculator.transform("~(1 + 1)")
        self.assertEqual(result, "0-(1+1)")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
