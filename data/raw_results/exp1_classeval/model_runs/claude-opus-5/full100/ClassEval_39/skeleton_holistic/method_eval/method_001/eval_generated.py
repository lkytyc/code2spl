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
        self.prepare(self.transform(expression))

        result_stack = deque()
        for token in self.postfix_stack:
            if self.is_operator(token):
                second_value = result_stack.pop()
                first_value = result_stack.pop()
                result = self._calculate(first_value, second_value, token)
                result_stack.append(str(result))
            else:
                result_stack.append(token)

        return float(result_stack.pop())

    def prepare(self, expression):
        """
        Prepare the infix expression for conversion to postfix notation
        :param expression: string, the infix expression to be prepared
        >>> expression_calculator = ExpressionCalculator()
        >>> expression_calculator.prepare("2+3*4")

        expression_calculator.postfix_stack = ['2', '3', '4', '*', '+']
        """
        op_stack = deque([','])
        arr = list(expression)
        current_index = 0
        count = 0

        for i, current_op in enumerate(arr):
            if not self.is_operator(current_op):
                count += 1
                if i == len(arr) - 1 or self.is_operator(arr[i + 1]):
                    self.postfix_stack.append(''.join(arr[current_index:current_index + count]))
                    count = 0
                    current_index = i + 1
            else:
                current_index = i + 1
                if current_op == ')':
                    while op_stack[-1] != '(':
                        self.postfix_stack.append(op_stack.pop())
                    op_stack.pop()  # remove '('
                else:
                    while self.compare(current_op, op_stack[-1]):
                        self.postfix_stack.append(op_stack.pop())
                    op_stack.append(current_op)

        while op_stack[-1] != ',':
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
        op_map = {',': 0, '(': 1, '+': 2, '-': 2, '*': 3, '/': 3, '%': 3}
        # Returns True if the peek operator has >= priority than cur (meaning we should pop peek first)
        return op_map.get(peek, 0) >= op_map.get(cur, 0)

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
        first = decimal.Decimal(first_value)
        second = decimal.Decimal(second_value)

        if current_op == '+':
            return float(first + second)
        elif current_op == '-':
            return float(first - second)
        elif current_op == '*':
            return float(first * second)
        elif current_op == '/':
            return float(first / second)
        elif current_op == '%':
            return float(first % second)
        else:
            raise ValueError(f"Unknown operator: {current_op}")

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
        expression = expression.replace(' ', '')
        result = []
        for i, c in enumerate(expression):
            if c == '-':
                if i == 0 or expression[i - 1] == '(':
                    result.append('0')
            result.append(c)
        return ''.join(result)

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
