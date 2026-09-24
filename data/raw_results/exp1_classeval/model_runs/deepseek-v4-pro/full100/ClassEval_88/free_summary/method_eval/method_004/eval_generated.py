class TriCalculator:
    def cos(self, x):
        return round(self.taylor(x, 50), 10)

    def factorial(self, a):
        result = 1
        for i in range(1, a + 1):
            result *= i
        return result

    def taylor(self, x, n):
        x = x * 3.141592653589793 / 180
        result = 0
        for i in range(n):
            term = (x ** (2 * i)) / self.factorial(2 * i)
            if i % 2 == 0:
                result += term
            else:
                result -= term
        return result

    def sin(self, x):
        x = x * 3.141592653589793 / 180
        result = 0
        term = x
        n = 1
        while abs(term) > 1e-15:
            result += term
            term = -term * x * x / ((2 * n) * (2 * n + 1))
            n += 1
        return round(result, 10)

    def tan(self, x):
        c = self.cos(x)
        if c == 0:
            return False
        return round(self.sin(x) / c, 10)

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
