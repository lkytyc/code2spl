class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            '^': lambda a, b: a ** b,
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
        if op == '^':
            operands.append(self.operators[op](a, b))
        else:
            operands.append(self.operators[op](a, b))

    def calculate(self, expression):
        operands = []
        operators = []
        i = 0
        num_buffer = ''

        while i < len(expression):
            ch = expression[i]

            if ch.isdigit() or ch == '.':
                num_buffer += ch
            else:
                if num_buffer:
                    operands.append(float(num_buffer))
                    num_buffer = ''

                if ch == '(':
                    operators.append(ch)
                elif ch == ')':
                    while operators and operators[-1] != '(':
                        self.apply_operator(operands, operators)
                    if operators:
                        operators.pop()  # remove '('
                elif ch in self.operators:
                    while (operators and
                           operators[-1] != '(' and
                           self.precedence(operators[-1]) >= self.precedence(ch)):
                        self.apply_operator(operands, operators)
                    operators.append(ch)

            i += 1

        if num_buffer:
            operands.append(float(num_buffer))

        while operators:
            self.apply_operator(operands, operators)

        return operands[-1] if operands else None

import unittest

class CalculatorTestCalculate(unittest.TestCase):
    def test_calculate_1(self):
        calculator = Calculator()
        res = calculator.calculate('1+2')
        self.assertEqual(res, 3)

    def test_calculate_2(self):
        calculator = Calculator()
        res = calculator.calculate('1+2*3')
        self.assertEqual(res, 7)

    def test_calculate_3(self):
        calculator = Calculator()
        res = calculator.calculate('1+2*3+4')
        self.assertEqual(res, 11)

    def test_calculate_4(self):
        calculator = Calculator()
        res = calculator.calculate('1+2^3*2+4*5')
        self.assertEqual(res, 37)

    def test_calculate_5(self):
        calculator = Calculator()
        res = calculator.calculate('1+2+3')
        self.assertEqual(res, 6)

    def test_calculate_6(self):
        calculator = Calculator()
        res = calculator.calculate('(1+2)+3')
        self.assertEqual(res, 6)

    def test_calculate_7(self):
        calculator = Calculator()
        res = calculator.calculate('')
        self.assertEqual(res, None)

    def test_calculate_8(self):
        calculator = Calculator()
        res = calculator.calculate('1+2?')
        self.assertEqual(res, 3)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
