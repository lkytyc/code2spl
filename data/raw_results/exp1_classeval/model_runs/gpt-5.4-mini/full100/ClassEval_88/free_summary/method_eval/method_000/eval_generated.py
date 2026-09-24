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

class TriCalculatorTestCos(unittest.TestCase):
    def test_cos_1(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.cos(60), 0.5)

    def test_cos_2(self):
        tricalculator = TriCalculator()
        self.assertAlmostEqual(tricalculator.cos(30), 0.8660254038)

    def test_cos_3(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.cos(0), 1.0)

    def test_cos_4(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.cos(90), 0.0)

    def test_cos_5(self):
        tricalculator = TriCalculator()
        self.assertAlmostEqual(tricalculator.cos(45), 0.7071067812)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
