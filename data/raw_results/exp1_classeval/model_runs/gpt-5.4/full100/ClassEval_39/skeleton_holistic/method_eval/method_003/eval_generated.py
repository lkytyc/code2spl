from collections import deque
from decimal import Decimal


class ExpressionCalculator:
    """
    This is a class in Python that can perform calculations with basic arithmetic operations, including addition, subtraction, multiplication, division, and modulo.
    """

    def __init__(self):
        """
        Initialize the expression calculator
        """
        self.postfix_stack = deque()
        self.operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]

    def calculate(self, expression):
        """
        Calculate the result of the given postfix expression
        :param expression: string, the postfix expression to be calculated
        :return: float, the calculated result
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.calculate("2 + 3 * 4")
        14.0

        """
        self.prepare(expression)
        stack = deque()
        for token in self.postfix_stack:
            if self.is_operator(token):
                second_value = stack.pop()
                first_value = stack.pop()
                stack.append(self._calculate(first_value, second_value, token))
            else:
                stack.append(Decimal(str(token)))
        return float(stack.pop())

    def prepare(self, expression):
        """
        Prepare the infix expression for conversion to postfix notation
        :param expression: string, the infix expression to be prepared
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.prepare("2+3*4")

        expression_calculator.postfix_stack = ['2', '3', '4', '*', '+']
        """
        expression = self.transform(expression)
        self.postfix_stack = deque()
        op_stack = deque()
        number = ""

        for c in expression:
            if c.isdigit() or c == '.':
                number += c
            else:
                if number:
                    self.postfix_stack.append(number)
                    number = ""
                if self.is_operator(c):
                    if c == '(':
                        op_stack.append(c)
                    elif c == ')':
                        while op_stack and op_stack[-1] != '(':
                            self.postfix_stack.append(op_stack.pop())
                        if op_stack and op_stack[-1] == '(':
                            op_stack.pop()
                    else:
                        while op_stack and op_stack[-1] != '(' and self.compare(c, op_stack[-1]):
                            self.postfix_stack.append(op_stack.pop())
                        op_stack.append(c)

        if number:
            self.postfix_stack.append(number)

        while op_stack:
            self.postfix_stack.append(op_stack.pop())

    @staticmethod
    def is_operator(c):
        """
        Check if a character is an operator in {'+', '-', '*', '/', '(', ')', '%'}
        :param c: string, the character to be checked
        :return: bool, True if the character is an operator, False otherwise
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.is_operator("+")
        True

        """
        return c in {'+', '-', '*', '/', '(', ')', '%'}

    def compare(self, cur, peek):
        """
        Compare the precedence of two operators
        :param cur: string, the current operator
        :param peek: string, the operator at the top of the operator stack
        :return: bool, True if the current operator has higher or equal precedence, False otherwise
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.compare("+", "-")
        True

        """
        priority = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '(': 0, ')': 0}
        return priority[cur] <= priority[peek]

    @staticmethod
    def _calculate(first_value, second_value, current_op):
        """
        Perform the mathematical calculation based on the given operands and operator
        :param first_value: string, the first operand
        :param second_value: string, the second operand
        :param current_op: string, the operator
        :return: decimal.Decimal, the calculated result
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator._calculate("2", "3", "+")
        5.0

        """
        first_value = Decimal(str(first_value))
        second_value = Decimal(str(second_value))
        if current_op == '+':
            return first_value + second_value
        if current_op == '-':
            return first_value - second_value
        if current_op == '*':
            return first_value * second_value
        if current_op == '/':
            return first_value / second_value
        if current_op == '%':
            return first_value % second_value
        raise ValueError("Unsupported operator")

    @staticmethod
    def transform(expression):
        """
        Transform the infix expression to a format suitable for conversion
        :param expression: string, the infix expression to be transformed
        :return: string, the transformed expression
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.transform("2 + 3 * 4")
        "2+3*4"

        """
        return expression.replace(" ", "")

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
