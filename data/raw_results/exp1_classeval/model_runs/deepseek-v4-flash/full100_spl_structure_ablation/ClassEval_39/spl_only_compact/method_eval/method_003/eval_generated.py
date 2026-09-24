from collections import deque
from decimal import Decimal

class ExpressionCalculator:
    def __init__(self):
        self.postfix_stack = deque()
        self.operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]

    def _calculate(self, first_value, second_value, current_op):
        if current_op == '+':
            return Decimal(first_value) + Decimal(second_value)
        elif current_op == '-':
            return Decimal(first_value) - Decimal(second_value)
        elif current_op == '*':
            return Decimal(first_value) * Decimal(second_value)
        elif current_op == '/':
            return Decimal(first_value) / Decimal(second_value)
        elif current_op == '%':
            return Decimal(first_value) % Decimal(second_value)
        else:
            raise ValueError(f"Unexpected operator: {current_op}")

    def calculate(self, expression):
        self.prepare(self.transform(expression))
        result_stack = deque()
        self.postfix_stack.reverse()
        while self.postfix_stack:
            current_op = self.postfix_stack.pop()
            if not self.is_operator(current_op):
                result_stack.append(current_op.replace('~', '-'))
            else:
                second_value = result_stack.pop()
                first_value = result_stack.pop()
                first_value = first_value.replace('~', '-')
                second_value = second_value.replace('~', '-')
                temp_result = self._calculate(first_value, second_value, current_op)
                result_stack.append(str(temp_result))
        return float(eval('*'.join(result_stack)))

    def compare(self, cur, peek):
        if cur == '%':
            cur = '/'
        if peek == '%':
            peek = '/'
        peek_precedence = self.operat_priority[ord(peek) - 40]
        cur_precedence = self.operat_priority[ord(cur) - 40]
        return peek_precedence >= cur_precedence

    def is_operator(self, c):
        return c in {'+', '-', '*', '/', '(', ')', '%'}

    def prepare(self, expression):
        op_stack = deque([','])
        arr = list(expression)
        current_index = 0
        count = 0
        for i, current_op in enumerate(arr):
            operator_check = self.is_operator(current_op)
            if not operator_check:
                count += 1
            else:
                if count > 0:
                    self.postfix_stack.append(''.join(arr[current_index:current_index + count]))
                peek_op = op_stack[-1]
                if current_op == ')':
                    while op_stack[-1] != '(':
                        popped_operator = op_stack.pop()
                        self.postfix_stack.append(str(popped_operator))
                    op_stack.pop()  # discard '('
                if current_op != ')':
                    while current_op != '(' and peek_op != ',' and self.compare(current_op, peek_op):
                        popped_operator = op_stack.pop()
                        self.postfix_stack.append(str(popped_operator))
                        peek_op = op_stack[-1]
                    op_stack.append(current_op)
                count = 0
                current_index = i + 1
        if count > 1 or (count == 1 and not self.is_operator(arr[current_index])):
            self.postfix_stack.append(''.join(arr[current_index:current_index + count]))
        while op_stack[-1] != ',':
            popped_operator = op_stack.pop()
            self.postfix_stack.append(str(popped_operator))

    def transform(self, expression):
        # The specification mentions transform but doesn't provide its implementation.
        # Based on the calculate method, transform is called before prepare.
        # Since no details are given, we'll return the expression as-is.
        return expression

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
