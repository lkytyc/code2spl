class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            '^': lambda a, b: a ** b
        }

    def precedence(self, op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        if op == '^':
            return 3
        return 0

    def apply_operator(self, operands, operators):
        op = operators.pop()
        b = operands.pop()
        a = operands.pop()
        operands.append(self.operators[op](a, b))

    def calculate(self, expression):
        operands = []
        operators = []
        i = 0
        while i < len(expression):
            ch = expression[i]
            if ch.isdigit() or ch == '.':
                num_str = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                operands.append(float(num_str))
                continue
            elif ch == '(':
                operators.append(ch)
            elif ch == ')':
                while operators and operators[-1] != '(':
                    self.apply_operator(operands, operators)
                operators.pop()
            elif ch in self.operators:
                while (operators and operators[-1] != '(' and
                       self.precedence(operators[-1]) >= self.precedence(ch)):
                    self.apply_operator(operands, operators)
                operators.append(ch)
            i += 1
        while operators:
            self.apply_operator(operands, operators)
        return operands[-1] if operands else None

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
