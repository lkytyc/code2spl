class Calculator:
    """
    This is a class for a calculator, capable of performing basic arithmetic calculations on numerical expressions using the operators +, -, *, /, and ^ (exponentiation).
    """

    def __init__(self):
        """
        Initialize the operations performed by the five operators'+','-','*','/','^'
        """
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': lambda x, y: x ** y
        }

    def calculate(self, expression):
        """
        Calculate the value of a given expression
        :param expression: string, given expression
        :return:If successful, returns the value of the expression; otherwise, returns None
        >>> calculator = Calculator()
        >>> calculator.calculate('1+2-3')
        0.0
        """
        if not expression:
            return None

        operand_stack = []
        operator_stack = []
        i = 0
        while i < len(expression):
            char = expression[i]

            if char.isdigit() or char == '.':
                num_str = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                try:
                    operand_stack.append(float(num_str))
                except ValueError:
                    return None
                continue

            if char in self.operators:
                while (operator_stack and operator_stack[-1] in self.operators and
                       self.precedence(operator_stack[-1]) >= self.precedence(char)):
                    self.apply_operator(operand_stack, operator_stack)
                operator_stack.append(char)
                i += 1
                continue

            if char == '(':
                operator_stack.append(char)
                i += 1
                continue

            if char == ')':
                while operator_stack and operator_stack[-1] != '(':
                    self.apply_operator(operand_stack, operator_stack)
                if not operator_stack:
                    return None
                operator_stack.pop()
                i += 1
                continue

            return None

        while operator_stack:
            if operator_stack[-1] == '(':
                return None
            self.apply_operator(operand_stack, operator_stack)

        if len(operand_stack) == 1:
            return operand_stack[0]
        return None

    def precedence(self, operator):
        """
        Returns the priority of the specified operator, where the higher the priority, the greater the assignment. The priority of '^' is greater than '/' and '*', and the priority of '/' and '*' is greater than '+' and '-'
        :param operator: string, given operator
        :return: int, the priority of the given operator, otherwise return 0
        >>> calculator = Calculator()
        >>> calculator.precedence('+')
        1
        >>> calculator.precedence('^')
        3
        """
        if operator in ('+', '-'):
            return 1
        if operator in ('*', '/'):
            return 2
        if operator == '^':
            return 3
        return 0

    def apply_operator(self, operand_stack, operator_stack):
        """
        Use the operator at the top of the operator stack to perform the operation on the two numbers at the top of the operator stack, and store the results at the top of the operator stack
        :param operand_stack:list
        :param operator_stack:list
        :return: the updated operand_stack and operator_stack
        >>> calculator = Calculator()
        >>> calculator.apply_operator([1, 2, 3], ['+', '-'])
        ([1, -1], ['-'])
        """
        if len(operand_stack) < 2 or not operator_stack:
            return operand_stack, operator_stack

        operator = operator_stack.pop()
        right = operand_stack.pop()
        left = operand_stack.pop()

        if operator == '/' and right == 0:
            operand_stack.append(float('inf'))
        else:
            result = self.operators[operator](left, right)
            operand_stack.append(result)

        return operand_stack, operator_stack

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
