class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            '^': lambda a, b: a ** b,
        }

    def precedence(self, operator):
        if operator == '^':
            return 3
        if operator in ('*', '/'):
            return 2
        if operator in ('+', '-'):
            return 1
        return 0

    def apply_operator(self, operand_stack, operator_stack):
        operator = operator_stack.pop()
        right = operand_stack.pop()
        left = operand_stack.pop()
        operand_stack.append(self.operators[operator](left, right))

    def calculate(self, expression):
        operand_stack = []
        operator_stack = []
        number_buffer = []

        def flush_number():
            if number_buffer:
                operand_stack.append(float(''.join(number_buffer)))
                number_buffer.clear()

        i = 0
        while i < len(expression):
            ch = expression[i]

            if ch.isdigit() or ch == '.':
                number_buffer.append(ch)
            elif ch == ' ':
                flush_number()
            elif ch == '(':
                flush_number()
                operator_stack.append(ch)
            elif ch == ')':
                flush_number()
                while operator_stack and operator_stack[-1] != '(':
                    self.apply_operator(operand_stack, operator_stack)
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
            elif ch in self.operators:
                flush_number()
                while (
                    operator_stack and
                    operator_stack[-1] != '(' and
                    (
                        self.precedence(operator_stack[-1]) > self.precedence(ch) or
                        (self.precedence(operator_stack[-1]) == self.precedence(ch) and ch != '^')
                    )
                ):
                    self.apply_operator(operand_stack, operator_stack)
                operator_stack.append(ch)
            i += 1

        flush_number()

        while operator_stack:
            self.apply_operator(operand_stack, operator_stack)

        return operand_stack[0] if operand_stack else None

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
