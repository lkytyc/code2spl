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
        if not isinstance(expression, str) or not expression:
            return None

        expression = expression.replace(" ", "")
        if not expression:
            return None

        operand_stack = []
        operator_stack = []
        i = 0
        n = len(expression)

        try:
            while i < n:
                char = expression[i]

                if char.isdigit() or char == '.':
                    j = i
                    dot_count = 0
                    while j < n and (expression[j].isdigit() or expression[j] == '.'):
                        if expression[j] == '.':
                            dot_count += 1
                            if dot_count > 1:
                                return None
                        j += 1
                    operand_stack.append(float(expression[i:j]))
                    i = j
                    continue

                if char in self.operators:
                    if char == '-' and (i == 0 or expression[i - 1] in self.operators):
                        j = i + 1
                        if j >= n:
                            return None
                        dot_count = 0
                        if expression[j] == '.':
                            dot_count = 1
                            j += 1
                        while j < n and (expression[j].isdigit() or expression[j] == '.'):
                            if expression[j] == '.':
                                dot_count += 1
                                if dot_count > 1:
                                    return None
                            j += 1
                        if j == i + 1 or (j == i + 2 and expression[i + 1] == '.'):
                            return None
                        operand_stack.append(float(expression[i:j]))
                        i = j
                        continue

                    while (operator_stack and
                           ((char != '^' and self.precedence(operator_stack[-1]) >= self.precedence(char)) or
                            (char == '^' and self.precedence(operator_stack[-1]) > self.precedence(char)))):
                        operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)
                        if operand_stack is None:
                            return None

                    operator_stack.append(char)
                    i += 1
                    continue

                return None

            while operator_stack:
                operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)
                if operand_stack is None:
                    return None

            if len(operand_stack) != 1:
                return None

            return float(operand_stack[0])
        except Exception:
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
        if not operator_stack or len(operand_stack) < 2:
            return None, None

        operator = operator_stack.pop()
        right = operand_stack.pop()
        left = operand_stack.pop()

        try:
            result = self.operators[operator](left, right)
        except Exception:
            return None, None

        operand_stack.append(result)
        return operand_stack, operator_stack

import unittest

class CalculatorTestCalculate(unittest.TestCase):
    def test_calculate_1(self):
        calculator = Calculator()
        res = calculator.calculate('1+2')
        self.assertEqual(res, 3)

    def test_calculate_2(self):
        calculator = Calculator()
        res = calculator.calculate('1+2*3')
        self.assertEqual(res, 7)

    def test_calculate_3(self):
        calculator = Calculator()
        res = calculator.calculate('1+2*3+4')
        self.assertEqual(res, 11)

    def test_calculate_4(self):
        calculator = Calculator()
        res = calculator.calculate('1+2^3*2+4*5')
        self.assertEqual(res, 37)

    def test_calculate_5(self):
        calculator = Calculator()
        res = calculator.calculate('1+2+3')
        self.assertEqual(res, 6)

    def test_calculate_6(self):
        calculator = Calculator()
        res = calculator.calculate('(1+2)+3')
        self.assertEqual(res, 6)

    def test_calculate_7(self):
        calculator = Calculator()
        res = calculator.calculate('')
        self.assertEqual(res, None)

    def test_calculate_8(self):
        calculator = Calculator()
        res = calculator.calculate('1+2?')
        self.assertEqual(res, 3)


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


class CalculatorTestApplyOperator(unittest.TestCase):
    def test_apply_operator_1(self):
        calculator = Calculator()
        operand_stack = [1, 2, 3]
        operator_stack = ['+', '-']
        calculator.apply_operator(operand_stack, operator_stack)
        self.assertEqual(operand_stack, [1, -1])
        self.assertEqual(operator_stack, ['+'])

    def test_apply_operator_2(self):
        calculator = Calculator()
        operand_stack = [1, 2, 3]
        operator_stack = ['+', '*']
        calculator.apply_operator(operand_stack, operator_stack)
        self.assertEqual(operand_stack, [1, 6])
        self.assertEqual(operator_stack, ['+'])

    def test_apply_operator_3(self):
        calculator = Calculator()
        operand_stack = [6, 3, 3]
        operator_stack = ['+', '/']
        calculator.apply_operator(operand_stack, operator_stack)
        self.assertEqual(operand_stack, [6, 1])
        self.assertEqual(operator_stack, ['+'])

    def test_apply_operator_4(self):
        calculator = Calculator()
        operand_stack = [1, 2, 3]
        operator_stack = ['+', '^']
        calculator.apply_operator(operand_stack, operator_stack)
        self.assertEqual(operand_stack, [1, 8])
        self.assertEqual(operator_stack, ['+'])

    def test_apply_operator_5(self):
        calculator = Calculator()
        operand_stack = [1, 2, 3]
        operator_stack = ['+', '+']
        calculator.apply_operator(operand_stack, operator_stack)
        self.assertEqual(operand_stack, [1, 5])
        self.assertEqual(operator_stack, ['+'])


class CalculatorTest(unittest.TestCase):
    def test_calculator(self):
        calculator = Calculator()
        res = calculator.calculate('1+2')
        self.assertEqual(res, 3)
        res1 = calculator.precedence('+')
        res2 = calculator.precedence('-')
        res3 = calculator.precedence('*')
        res4 = calculator.precedence('/')
        res5 = calculator.precedence('^')
        self.assertEqual(res1, res2)
        self.assertEqual(res3, res4)
        self.assertGreater(res3, res1)
        self.assertGreater(res5, res3)
        operand_stack = [1, 2, 3]
        operator_stack = ['+', '-']
        calculator.apply_operator(operand_stack, operator_stack)
        self.assertEqual(operand_stack, [1, -1])
        self.assertEqual(operator_stack, ['+'])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
