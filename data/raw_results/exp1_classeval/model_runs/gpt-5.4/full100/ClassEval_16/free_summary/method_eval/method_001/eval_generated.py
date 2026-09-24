import operator


class Calculator:
    def __init__(self):
        self.operations = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '^': operator.pow,
        }

    def precedence(self, operator_symbol):
        if operator_symbol in ('+', '-'):
            return 1
        if operator_symbol in ('*', '/'):
            return 2
        if operator_symbol == '^':
            return 3
        return 0

    def apply_operator(self, operand_stack, operator_stack):
        if len(operand_stack) < 2 or not operator_stack:
            return
        right = operand_stack.pop()
        left = operand_stack.pop()
        op = operator_stack.pop()
        result = self.operations[op](left, right)
        operand_stack.append(float(result))

    def calculate(self, expression):
        operand_stack = []
        operator_stack = []
        i = 0
        n = len(expression)

        while i < n:
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char.isdigit() or char == '.':
                num_str = []
                dot_count = 0
                while i < n and (expression[i].isdigit() or expression[i] == '.'):
                    if expression[i] == '.':
                        dot_count += 1
                    num_str.append(expression[i])
                    i += 1
                if dot_count <= 1 and num_str and num_str != ['.']:
                    operand_stack.append(float(''.join(num_str)))
                continue

            if char == '(':
                operator_stack.append(char)

            elif char == ')':
                while operator_stack and operator_stack[-1] != '(':
                    self.apply_operator(operand_stack, operator_stack)
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()

            elif char in self.operations:
                while (
                    operator_stack
                    and operator_stack[-1] != '('
                    and (
                        self.precedence(operator_stack[-1]) > self.precedence(char)
                        or (
                            self.precedence(operator_stack[-1]) == self.precedence(char)
                            and char != '^'
                        )
                    )
                ):
                    self.apply_operator(operand_stack, operator_stack)
                operator_stack.append(char)

            i += 1

        while operator_stack:
            if operator_stack[-1] == '(':
                operator_stack.pop()
            else:
                self.apply_operator(operand_stack, operator_stack)

        return float(operand_stack[-1]) if operand_stack else None

import unittest

class CalculatorTestPrecedence(unittest.TestCase):
    def test_precedence_1(self):
        calculator = Calculator()
        res1 = calculator.precedence('+')
        res2 = calculator.precedence('-')
        self.assertEqual(res1, res2)

    def test_precedence_2(self):
        calculator = Calculator()
        res1 = calculator.precedence('*')
        res2 = calculator.precedence('/')
        self.assertEqual(res1, res2)

    def test_precedence_3(self):
        calculator = Calculator()
        res1 = calculator.precedence('+')
        res2 = calculator.precedence('/')
        self.assertNotEqual(res1, res2)

    def test_precedence_4(self):
        calculator = Calculator()
        res1 = calculator.precedence('+')
        res2 = calculator.precedence('/')
        self.assertNotEqual(res1, res2)

    def test_precedence_5(self):
        calculator = Calculator()
        res1 = calculator.precedence('*')
        res2 = calculator.precedence('-')
        self.assertNotEqual(res1, res2)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
