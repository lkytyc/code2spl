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

class TriCalculatorTestTan(unittest.TestCase):
    def test_tan_1(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.tan(45), 1.0)

    def test_tan_2(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.tan(90), False)

    def test_tan_3(self):
        tricalculator = TriCalculator()
        self.assertAlmostEqual(tricalculator.tan(30), 0.5773502692)

    def test_tan_4(self):
        tricalculator = TriCalculator()
        self.assertAlmostEqual(tricalculator.tan(60), 1.7320508076)

    def test_tan_5(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.tan(0), 0.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
