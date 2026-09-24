from collections import deque
from decimal import Decimal
import re


class ExpressionCalculator:
    def __init__(self):
        self.postfix_stack = deque()
        self.operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]

    def calculate(self, expression):
        self.postfix_stack.clear()
        self.prepare(self.transform(expression))
        result_stack = deque()
        self.postfix_stack.reverse()

        while self.postfix_stack:
            current_op = self.postfix_stack.pop()
            if not self.is_operator(current_op):
                result_stack.append(current_op.replace("~", "-"))
            else:
                second_value = result_stack.pop()
                first_value = result_stack.pop()
                first_value = first_value.replace("~", "-")
                second_value = second_value.replace("~", "-")
                temp_result = self._calculate(first_value, second_value, current_op)
                result_stack.append(str(temp_result))

        return float(eval("*".join(result_stack)))

    def prepare(self, expression):
        op_stack = deque([","])
        arr = list(expression)
        current_index = 0
        count = 0

        for i, current_op in enumerate(arr):
            if self.is_operator(current_op):
                if count > 0:
                    self.postfix_stack.append("".join(arr[current_index: current_index + count]))
                peek_op = op_stack[-1]
                if current_op == ")":
                    while op_stack[-1] != "(":
                        self.postfix_stack.append(str(op_stack.pop()))
                    op_stack.pop()
                else:
                    while current_op != "(" and peek_op != "," and self.compare(current_op, peek_op):
                        self.postfix_stack.append(str(op_stack.pop()))
                        peek_op = op_stack[-1]
                    op_stack.append(current_op)
                count = 0
                current_index = i + 1
            else:
                count += 1

        if count > 1 or (count == 1 and not self.is_operator(arr[current_index])):
            self.postfix_stack.append("".join(arr[current_index: current_index + count]))

        while op_stack[-1] != ",":
            self.postfix_stack.append(str(op_stack.pop()))

    def is_operator(self, c):
        return c in {"+", "-", "*", "/", "(", ")", "%"}

    def compare(self, cur, peek):
        if cur == "%":
            cur = "/"
        if peek == "%":
            peek = "/"
        peek_priority = self.operat_priority[ord(peek) - 40]
        cur_priority = self.operat_priority[ord(cur) - 40]
        return peek_priority >= cur_priority

    def _calculate(self, first_value, second_value, current_op):
        if current_op == "+":
            return Decimal(first_value) + Decimal(second_value)
        if current_op == "-":
            return Decimal(first_value) - Decimal(second_value)
        if current_op == "*":
            return Decimal(first_value) * Decimal(second_value)
        if current_op == "/":
            return Decimal(first_value) / Decimal(second_value)
        if current_op == "%":
            return Decimal(first_value) % Decimal(second_value)
        raise ValueError(f"Unexpected operator: {current_op}")

    def transform(self, expression):
        expression = re.sub(r"\s+", "", expression)
        expression = re.sub(r"=$", "", expression)
        arr = list(expression)

        for i, c in enumerate(arr):
            if c == "-":
                if i == 0:
                    arr[i] = "~"
                else:
                    prev_c = arr[i - 1]
                    if prev_c in {"+", "-", "*", "/", "(", "E", "e"}:
                        arr[i] = "~"

        if arr[0] == "~" and (len(arr) > 1 and arr[1] == "("):
            arr[0] = "-"
            return "0" + "".join(arr)
        return "".join(arr)

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
