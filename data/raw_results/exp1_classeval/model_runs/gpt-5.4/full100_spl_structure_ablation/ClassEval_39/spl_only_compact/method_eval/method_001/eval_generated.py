class ExpressionCalculator:
    def __init__(self):
        from collections import deque

        self.postfix_stack = deque()
        self.operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]

    def _calculate(self, first_value, second_value, current_op):
        from decimal import Decimal
        import logging

        if current_op == "+":
            result = Decimal(first_value) + Decimal(second_value)
            return result

        if current_op == "-":
            result = Decimal(first_value) - Decimal(second_value)
            return result

        if current_op == "*":
            result = Decimal(first_value) * Decimal(second_value)
            return result

        if current_op == "/":
            result = Decimal(first_value) / Decimal(second_value)
            return result

        if current_op == "%":
            result = Decimal(first_value) % Decimal(second_value)
            return result

        logging.error("Unexpected operator: %s", current_op)
        raise ValueError("Raised when the operator is unsupported.")

    def calculate(self, expression):
        from collections import deque

        self.prepare(self.transform(expression))
        result_stack = deque()
        self.postfix_stack.reverse()

        while self.postfix_stack:
            current_op = self.postfix_stack.pop()

            if not self.is_operator(current_op):
                current_op = current_op.replace("~", "-")
                result_stack.append(current_op)
            else:
                second_value = result_stack.pop()
                first_value = result_stack.pop()

                first_value = first_value.replace("~", "-")
                second_value = second_value.replace("~", "-")

                temp_result = self._calculate(
                    first_value,
                    second_value,
                    current_op,
                )
                result_stack.append(str(temp_result))

        final_result = eval("*".join(result_stack))
        return float(final_result)

    def compare(self, cur, peek):
        if cur == "%":
            cur = "/"

        if peek == "%":
            peek = "/"

        peek_priority = self.operat_priority[ord(peek) - 40]
        cur_priority = self.operat_priority[ord(cur) - 40]

        return peek_priority >= cur_priority

    def is_operator(self, c):
        return c in {"+", "-", "*", "/", "(", ")", "%"}

    def prepare(self, expression):
        from collections import deque

        op_stack = deque([","])
        arr = list(expression)
        current_index = 0
        count = 0

        for i, current_op in enumerate(arr):
            if self.is_operator(current_op):
                if count > 0:
                    self.postfix_stack.append(
                        "".join(arr[current_index:current_index + count])
                    )

                peek_op = op_stack[-1]

                if current_op == ")":
                    while op_stack[-1] != "(":
                        self.postfix_stack.append(str(op_stack.pop()))
                    op_stack.pop()
                else:
                    while (
                        current_op != "("
                        and peek_op != ","
                        and self.compare(current_op, peek_op)
                    ):
                        self.postfix_stack.append(str(op_stack.pop()))
                        peek_op = op_stack[-1]

                    op_stack.append(current_op)

                count = 0
                current_index = i + 1
            else:
                count += 1

        if (
            count > 1
            or (count == 1 and not self.is_operator(arr[current_index]))
        ):
            self.postfix_stack.append(
                "".join(arr[current_index:current_index + count])
            )

        while op_stack[-1] != ",":
            self.postfix_stack.append(str(op_stack.pop()))

    def transform(self, expression):
        import re

        expression = re.sub(r"\s+", "", expression)
        expression = re.sub(r"=$", "", expression)
        arr = list(expression)

        for i, c in enumerate(arr):
            if c != "-":
                continue

            if i == 0:
                arr[i] = "~"
            else:
                prev_c = arr[i - 1]
                if prev_c in {"+", "-", "*", "/", "(", "E", "e"}:
                    arr[i] = "~"

        if arr[0] == "~" and len(arr) > 1 and arr[1] == "(":
            arr[0] = "-"
            return "0" + "".join(arr)

        return "".join(arr)

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
