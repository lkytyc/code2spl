from decimal import Decimal


class ExpressionCalculator:
    operat_priority = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '%': 2,
        '(': 0,
        ')': 0,
    }

    def __init__(self):
        self.postfix_stack = []

    def is_operator(self, char):
        return char in ['+', '-', '*', '/', '%', '(', ')']

    def compare(self, cur, top):
        return self.operat_priority[cur] <= self.operat_priority[top]

    def transform(self, expression):
        expression = expression.replace(' ', '')
        if expression.endswith('='):
            expression = expression[:-1]

        if expression.startswith('-('):
            expression = '0' + expression

        result = []
        for i, ch in enumerate(expression):
            if ch == '-':
                if i == 0:
                    result.append('~')
                else:
                    prev = expression[i - 1]
                    if prev in ['+', '-', '*', '/', '(', 'E', 'e']:
                        result.append('~')
                    else:
                        result.append(ch)
            else:
                result.append(ch)
        return ''.join(result)

    def prepare(self, expression):
        op_stack = []
        i = 0
        n = len(expression)

        while i < n:
            ch = expression[i]

            if self.is_operator(ch):
                if ch == '(':
                    op_stack.append(ch)
                elif ch == ')':
                    while op_stack and op_stack[-1] != '(':
                        self.postfix_stack.append(op_stack.pop())
                    if op_stack and op_stack[-1] == '(':
                        op_stack.pop()
                else:
                    while op_stack and op_stack[-1] != '(' and self.compare(ch, op_stack[-1]):
                        self.postfix_stack.append(op_stack.pop())
                    op_stack.append(ch)
                i += 1
            else:
                token = []
                while i < n and not self.is_operator(expression[i]):
                    token.append(expression[i])
                    i += 1
                self.postfix_stack.append(''.join(token))

        while op_stack:
            self.postfix_stack.append(op_stack.pop())

    def _calculate(self, left, right, operator):
        left_d = Decimal(left.replace('~', '-'))
        right_d = Decimal(right.replace('~', '-'))

        if operator == '+':
            return str(left_d + right_d)
        if operator == '-':
            return str(left_d - right_d)
        if operator == '*':
            return str(left_d * right_d)
        if operator == '/':
            return str(left_d / right_d)
        if operator == '%':
            return str(left_d % right_d)
        raise ValueError('Unsupported operator: ' + operator)

    def calculate(self, expression):
        expression = self.transform(expression)
        self.prepare(expression)

        result_stack = []
        for token in self.postfix_stack:
            if self.is_operator(token):
                right = result_stack.pop()
                left = result_stack.pop()
                result_stack.append(self._calculate(left, right, token))
            else:
                result_stack.append(token)

        return float(eval('*'.join(item.replace('~', '-') for item in result_stack)))

import unittest

class ExpressionCalculatorTestPrepare(unittest.TestCase):
    def setUp(self):
        self.expression_calculator = ExpressionCalculator()

    def test_prepare_1(self):
        self.expression_calculator.prepare("2+3*4")
        self.assertEqual(self.expression_calculator.postfix_stack, deque(['2', '3', '4', '*', '+']))

    def test_prepare_2(self):
        self.expression_calculator.prepare("2+3/4")
        self.assertEqual(self.expression_calculator.postfix_stack, deque(['2', '3', '4', '/', '+']))

    def test_prepare_3(self):
        self.expression_calculator.prepare("2-3*4")
        self.assertEqual(self.expression_calculator.postfix_stack, deque(['2', '3', '4', '*', '-']))

    def test_prepare_4(self):
        self.expression_calculator.prepare("1+3*4")
        self.assertEqual(self.expression_calculator.postfix_stack, deque(['1', '3', '4', '*', '+']))

    def test_prepare_5(self):
        self.expression_calculator.prepare("(2+3)*4")
        self.assertEqual(self.expression_calculator.postfix_stack, deque(['2', '3', '+', '4', '*']))

    def test_prepare_6(self):
        self.expression_calculator.prepare("")
        self.assertEqual(self.expression_calculator.postfix_stack, deque([]))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
