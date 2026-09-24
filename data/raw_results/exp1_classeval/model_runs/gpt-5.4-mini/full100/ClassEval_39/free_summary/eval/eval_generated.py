class ExpressionCalculator:
    def __init__(self):
        self.postfix_stack = []

    def is_operator(self, ch):
        return ch in {"+", "-", "*", "/", "%", "~"}

    def compare(self, op1, op2):
        precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "%": 2,
            "~": 3,
        }
        return precedence.get(op1, 0) - precedence.get(op2, 0)

    def transform(self, expression):
        if expression is None:
            expression = ""
        expression = "".join(expression.split())
        if expression.endswith("="):
            expression = expression[:-1]

        if not expression:
            return expression

        chars = list(expression)
        result = []

        for i, ch in enumerate(chars):
            if ch == "-":
                prev = chars[i - 1] if i > 0 else ""
                if i == 0 or prev in "+-*/%(":
                    if i + 1 < len(chars) and chars[i + 1] == "(":
                        result.append("0")
                    else:
                        result.append("~")
                    continue
            result.append(ch)

        return "".join(result)

    def prepare(self, expression):
        self.postfix_stack = []
        op_stack = []
        i = 0
        while i < len(expression):
            ch = expression[i]
            if ch.isdigit() or ch == ".":
                num = [ch]
                i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                    num.append(expression[i])
                    i += 1
                self.postfix_stack.append("".join(num))
                continue
            elif ch == "(":
                op_stack.append(ch)
            elif ch == ")":
                while op_stack and op_stack[-1] != "(":
                    self.postfix_stack.append(op_stack.pop())
                if op_stack and op_stack[-1] == "(":
                    op_stack.pop()
            elif self.is_operator(ch):
                while op_stack and op_stack[-1] != "(" and self.compare(op_stack[-1], ch) >= 0:
                    self.postfix_stack.append(op_stack.pop())
                op_stack.append(ch)
            i += 1

        while op_stack:
            self.postfix_stack.append(op_stack.pop())

    def _calculate(self, a, b, op):
        from decimal import Decimal
        a = Decimal(str(a))
        b = Decimal(str(b))

        if op == "+":
            return a + b
        if op == "-":
            return a - b
        if op == "*":
            return a * b
        if op == "/":
            return a / b
        if op == "%":
            return a % b
        raise ValueError(f"Unexpected operator: {op}")

    def calculate(self, expression):
        expression = self.transform(expression)
        self.prepare(expression)

        stack = []
        for token in self.postfix_stack:
            if token == "~":
                stack.append("-")
            elif token and (token[0].isdigit() or token[0] == ".") or (token.startswith("-") and len(token) > 1):
                stack.append(token)
            elif self.is_operator(token):
                b = stack.pop()
                a = stack.pop()
                if a == "-":
                    a = 0
                if b == "-":
                    b = 0
                res = self._calculate(a, b, token)
                stack.append(res)
            else:
                stack.append(token)

        return float(stack[-1])

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


class ExpressionCalculatorTestCalculateMethod(unittest.TestCase):
    def setUp(self):
        self.expression_calculator = ExpressionCalculator()

    def test_calculate_method_1(self):
        result = self.expression_calculator._calculate("2", "3", "+")
        self.assertEqual(result, Decimal(5.0))

    def test_calculate_method_2(self):
        result = self.expression_calculator._calculate("3", "2", "-")
        self.assertEqual(result, Decimal(1.0))

    def test_calculate_method_3(self):
        result = self.expression_calculator._calculate("2", "3", "*")
        self.assertEqual(result, Decimal(6.0))

    def test_calculate_method_4(self):
        result = self.expression_calculator._calculate("3", "3", "/")
        self.assertEqual(result, Decimal(1.0))

    def test_calculate_method_5(self):
        result = self.expression_calculator._calculate("6", "2", "/")
        self.assertEqual(result, Decimal(3.0))

    def test_calculate_method_6(self):
        result = self.expression_calculator._calculate("6", "2", "%")
        self.assertEqual(result, Decimal(0.0))

    def test_calculate_method_7(self):
        try:
            self.expression_calculator._calculate("6", "2", "??")
        except:
            pass


class ExpressionCalculatorTestTransform(unittest.TestCase):
    def setUp(self):
        self.expression_calculator = ExpressionCalculator()

    def test_transform_1(self):
        result = self.expression_calculator.transform("2 + 3 * 4")
        self.assertEqual(result, "2+3*4")

    def test_transform_2(self):
        result = self.expression_calculator.transform("2 + 3 / 4")
        self.assertEqual(result, "2+3/4")

    def test_transform_3(self):
        result = self.expression_calculator.transform("2 - 3 * 4")
        self.assertEqual(result, "2-3*4")

    def test_transform_4(self):
        result = self.expression_calculator.transform("1 + 3 * 4")
        self.assertEqual(result, "1+3*4")

    def test_transform_5(self):
        result = self.expression_calculator.transform("-2 + (-3) * 4")
        self.assertEqual(result, "~2+(~3)*4")

    def test_transform_6(self):
        result = self.expression_calculator.transform("~(1 + 1)")
        self.assertEqual(result, "0-(1+1)")


class ExpressionCalculatorTest(unittest.TestCase):
    def setUp(self):
        self.expression_calculator = ExpressionCalculator()

    def test_ExpressionCalculator(self):
        result = self.expression_calculator.calculate("2 + 3 * 4")
        self.assertEqual(result, 14.0)

        self.expression_calculator.prepare("2+3*4")
        self.assertEqual(self.expression_calculator.postfix_stack, deque(['2', '3', '4', '*', '+']))

        self.assertTrue(self.expression_calculator.is_operator("+"))

        result = self.expression_calculator.compare("+", "-")
        self.assertTrue(result)

        result = self.expression_calculator._calculate("2", "3", "+")
        self.assertEqual(result, Decimal(5.0))

        result = self.expression_calculator.transform("2 + 3 * 4")
        self.assertEqual(result, "2+3*4")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
