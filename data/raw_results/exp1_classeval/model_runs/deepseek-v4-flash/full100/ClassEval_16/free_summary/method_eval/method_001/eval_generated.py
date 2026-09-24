class Calculator:
    def __init__(self):
        self.precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '^': 3
        }
        self.operators = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            '^': lambda a, b: a ** b
        }

    def calculate(self, expression):
        operand_stack = []
        operator_stack = []
        i = 0

        while i < len(expression):
            char = expression[i]

            if char.isspace():
                i += 1
                continue

            if char.isdigit() or char == '.':
                number = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    number += expression[i]
                    i += 1
                operand_stack.append(float(number))
                continue

            if char == '(':
                operator_stack.append(char)
                i += 1
                continue

            if char == ')':
                while operator_stack and operator_stack[-1] != '(':
                    self.apply_operator(operator_stack, operand_stack)
                if operator_stack:
                    operator_stack.pop()
                i += 1
                continue

            if char in self.operators:
                while (
                    operator_stack
                    and operator_stack[-1] != '('
                    and self.precedence[operator_stack[-1]] >= self.precedence[char]
                ):
                    self.apply_operator(operator_stack, operand_stack)
                operator_stack.append(char)
                i += 1
                continue

            i += 1

        while operator_stack:
            self.apply_operator(operator_stack, operand_stack)

        if operand_stack:
            return operand_stack[-1]
        return None

    def apply_operator(self, operator_stack, operand_stack):
        operator = operator_stack.pop()
        right = operand_stack.pop()
        left = operand_stack.pop()
        operand_stack.append(self.operators[operator](left, right))

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
