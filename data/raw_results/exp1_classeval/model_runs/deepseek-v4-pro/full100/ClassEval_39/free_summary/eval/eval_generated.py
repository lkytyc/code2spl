class ExpressionCalculator:
    def __init__(self):
        self.postfix_stack = []
        self.operat_priority = [0] * 256
        self.operat_priority[ord('+')] = 1
        self.operat_priority[ord('-')] = 1
        self.operat_priority[ord('*')] = 2
        self.operat_priority[ord('/')] = 2
        self.operat_priority[ord('%')] = 2
        self.operat_priority[ord('~')] = 3

    @staticmethod
    def is_operator(c):
        return c in "+-*/%~"

    def compare(self, op1, op2):
        return self.operat_priority[ord(op1)] - self.operat_priority[ord(op2)]

    def transform(self, expression):
        expression = expression.replace(" ", "").rstrip("=")
        if not expression:
            return ""
        if expression[0] == '-':
            expression = "0" + expression
        result = []
        i = 0
        while i < len(expression):
            c = expression[i]
            if c == '-' and (i == 0 or expression[i-1] in "(+-*/%~"):
                result.append('~')
            else:
                result.append(c)
            i += 1
        return "".join(result)

    def prepare(self, expression):
        self.postfix_stack = []
        op_stack = []
        i = 0
        while i < len(expression):
            c = expression[i]
            if c.isdigit() or c == '.':
                j = i
                while j < len(expression) and (expression[j].isdigit() or expression[j] == '.'):
                    j += 1
                self.postfix_stack.append(expression[i:j])
                i = j
            elif c == '(':
                op_stack.append(c)
                i += 1
            elif c == ')':
                while op_stack and op_stack[-1] != '(':
                    self.postfix_stack.append(op_stack.pop())
                if op_stack:
                    op_stack.pop()
                i += 1
            elif self.is_operator(c):
                while op_stack and op_stack[-1] != '(' and self.compare(op_stack[-1], c) >= 0:
                    self.postfix_stack.append(op_stack.pop())
                op_stack.append(c)
                i += 1
            else:
                i += 1
        while op_stack:
            self.postfix_stack.append(op_stack.pop())

    @staticmethod
    def _calculate(op, left, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '%':
            return left % right
        elif op == '~':
            return -right
        else:
            raise ValueError("Unknown operator: " + op)

    def calculate(self, expression):
        transformed = self.transform(expression)
        self.prepare(transformed)
        result_stack = []
        for token in self.postfix_stack:
            if token in "+-*/%~":
                if token == '~':
                    right = result_stack.pop()
                    result_stack.append(self._calculate(token, None, right))
                else:
                    right = result_stack.pop()
                    left = result_stack.pop()
                    result_stack.append(self._calculate(token, left, right))
            else:
                result_stack.append(Decimal(token))
        return float(result_stack[0]) if result_stack else 0.0

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
