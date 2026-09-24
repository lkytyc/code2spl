import math

class TriCalculator:

    def cos(self, x):
        return self.taylor(x)

    def factorial(self, a):
        result = 1
        while a > 1:
            result *= a
            a -= 1
        return result

    def taylor(self, x):
        radians = x * math.pi / 180
        result = 0
        for k in range(50):
            sign = (-1) ** k
            numerator = radians ** (2 * k)
            denominator = self.factorial(2 * k)
            result += sign * numerator / denominator
        return round(result, 10)

    def sin(self, x):
        radians = x * math.pi / 180
        result = 0
        term = radians
        k = 1
        while abs(term) >= 1e-15:
            result += term
            k += 1
            term = term * (-1) * radians ** 2 / ((2 * k - 2) * (2 * k - 1))
        return round(result, 10)

    def tan(self, x):
        cos_val = self.cos(x)
        if cos_val == 0:
            return False
        return round(self.sin(x) / cos_val, 10)

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
