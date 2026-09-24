class TriCalculator:
    def __init__(self):
        pass

    def factorial(self, a):
        result = 1
        i = 1
        while i <= a:
            result *= i
            i += 1
        return result

    def taylor(self, x, n):
        import math
        x = x * math.pi / 180
        result = 1.0
        sign = -1
        i = 2
        while i < n:
            result += sign * (x ** i) / self.factorial(i)
            sign *= -1
            i += 2
        return result

    def cos(self, x):
        return round(self.taylor(x, 50), 10)

    def sin(self, x):
        import math
        x = x * math.pi / 180
        term = x
        result = 0.0
        n = 1
        while abs(term) >= 1e-15:
            result += term
            term *= -1 * x * x / ((2 * n) * (2 * n + 1))
            n += 1
        return round(result, 10)

    def tan(self, x):
        c = self.cos(x)
        if c != 0:
            return round(self.sin(x) / c, 10)
        return False

import unittest

class TriCalculatorTestFactorial(unittest.TestCase):
    def test_factorial_1(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.factorial(5), 120)

    def test_factorial_2(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.factorial(4), 24)

    def test_factorial_3(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.factorial(3), 6)

    def test_factorial_4(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.factorial(2), 2)

    def test_factorial_5(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.factorial(1), 1)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
