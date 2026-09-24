from collections import deque
from decimal import Decimal

class ExpressionCalculator:
    def __init__(self):
        self.postfix_stack = deque()
        self.operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]

    def calculate(self, expression: str) -> float:
        self.prepare(self.transform(expression))
        result_stack = deque()
        self.postfix_stack.reverse()
        while self.postfix_stack:
            current_op = self.postfix_stack.pop()
            if not self.is_operator(current_op):
                current_op = current_op.replace('~', '-')
                result_stack.append(current_op)
            else:
                second_value = result_stack.pop()
                first_value = result_stack.pop()
                first_value = first_value.replace('~', '-')
                second_value = second_value.replace('~', '-')
                temp_result = self._calculate(first_value, second_value, current_op)
                result_stack.append(str(temp_result))
        return float(eval('*'.join(result_stack)))

    def prepare(self, expression):
        op_stack = deque([','])
        arr = list(expression)
        current_index = 0
        count = 0
        for i, current_op in enumerate(arr):
            if self.is_operator(current_op):
                if count > 0:
                    self.postfix_stack.append(''.join(arr[current_index:current_index + count]))
                peek_op = op_stack[-1]
                if current_op == ')':
                    while op_stack[-1] != '(':
                        popped_operator = op_stack.pop()
                        self.postfix_stack.append(str(popped_operator))
                    op_stack.pop()  # discard '('
                else:
                    while current_op != '(' and peek_op != ',' and self.compare(current_op, peek_op):
                        popped_operator = op_stack.pop()
                        self.postfix_stack.append(str(popped_operator))
                        peek_op = op_stack[-1]
                    op_stack.append(current_op)
                count = 0
                current_index = i + 1
            else:
                count += 1
        if count > 1 or (count == 1 and not self.is_operator(arr[current_index])):
            self.postfix_stack.append(''.join(arr[current_index:current_index + count]))
        while op_stack[-1] != ',':
            popped_operator = op_stack.pop()
            self.postfix_stack.append(str(popped_operator))

    def is_operator(self, c) -> bool:
        return c in {'+', '-', '*', '/', '(', ')', '%'}

    def compare(self, cur: str, peek: str) -> bool:
        if cur == '%':
            cur = '/'
        if peek == '%':
            peek = '/'
        peek_precedence = self.operat_priority[ord(peek) - 40]
        cur_precedence = self.operat_priority[ord(cur) - 40]
        return peek_precedence >= cur_precedence

    def _calculate(self, first_value, second_value, current_op: str) -> Decimal:
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

    def transform(self, expression: str) -> str:
        # The SPL input for transform is missing, but based on the calculate method,
        # it transforms the expression. A reasonable implementation would replace
        # negative signs with '~' to avoid confusion with subtraction.
        # This is a common technique in such calculators.
        return expression.replace('-', '~') if expression.startswith('-') else expression

import unittest

class ExpressionCalculatorTestIsOperator(unittest.TestCase):
    def setUp(self):
        self.expression_calculator = ExpressionCalculator()

    def test_is_operator_1(self):
        self.assertTrue(self.expression_calculator.is_operator("+"))

    def test_is_operator_2(self):
        self.assertTrue(self.expression_calculator.is_operator("-"))

    def test_is_operator_3(self):
        self.assertTrue(self.expression_calculator.is_operator("*"))

    def test_is_operator_4(self):
        self.assertTrue(self.expression_calculator.is_operator("/"))

    def test_is_operator_5(self):
        self.assertFalse(self.expression_calculator.is_operator("5"))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
