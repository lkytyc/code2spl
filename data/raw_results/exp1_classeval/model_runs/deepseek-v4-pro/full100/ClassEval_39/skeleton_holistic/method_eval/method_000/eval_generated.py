from collections import deque
import decimal


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
            if not self.is_operator(token):
                stack.append(decimal.Decimal(token))
            else:
                second_value = stack.pop()
                first_value = stack.pop()
                result = self._calculate(first_value, second_value, token)
                stack.append(result)
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
        operator_stack = deque()
        self.postfix_stack = deque()
        i = 0
        while i < len(expression):
            c = expression[i]
            if c.isdigit() or c == '.':
                num = []
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num.append(expression[i])
                    i += 1
                self.postfix_stack.append(''.join(num))
                continue
            elif self.is_operator(c):
                if c == '(':
                    operator_stack.append(c)
                elif c == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        self.postfix_stack.append(operator_stack.pop())
                    if operator_stack:
                        operator_stack.pop()
                else:
                    while (operator_stack and operator_stack[-1] != '(' and
                           self.compare(operator_stack[-1], c)):
                        self.postfix_stack.append(operator_stack.pop())
                    operator_stack.append(c)
            i += 1
        while operator_stack:
            self.postfix_stack.append(operator_stack.pop())

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
        operators = ['+', '-', '*', '/', '%', '(', ')']
        cur_index = operators.index(cur)
        peek_index = operators.index(peek)
        return self.operat_priority[cur_index] >= self.operat_priority[peek_index]

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
        first_value = decimal.Decimal(first_value)
        second_value = decimal.Decimal(second_value)
        if current_op == '+':
            return first_value + second_value
        elif current_op == '-':
            return first_value - second_value
        elif current_op == '*':
            return first_value * second_value
        elif current_op == '/':
            return first_value / second_value
        elif current_op == '%':
            return first_value % second_value
        else:
            raise ValueError("Invalid operator")

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

class ExpressionCalculatorTestCalculate(unittest.TestCase):
    def setUp(self):
        self.expression_calculator = ExpressionCalculator()

    def test_calculate_1(self):
        result = self.expression_calculator.calculate("2 + 3 * 4")
        self.assertEqual(result, 14.0)

    def test_calculate_2(self):
        result = self.expression_calculator.calculate("2 + 3 + 4")
        self.assertEqual(result, 9.0)

    def test_calculate_3(self):
        result = self.expression_calculator.calculate("2 * 3 * 4")
        self.assertEqual(result, 24.0)

    def test_calculate_4(self):
        result = self.expression_calculator.calculate("2 + 4 / 4")
        self.assertEqual(result, 3.0)

    def test_calculate_5(self):
        result = self.expression_calculator.calculate("(2 + 3) * 4")
        self.assertEqual(result, 20.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
