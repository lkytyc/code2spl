class TriCalculator:
    def cos(self, x):
        return round(self.taylor(x, 50), 10)

    def factorial(self, a):
        if a == 0:
            return 1
        result = 1
        for i in range(2, a + 1):
            result *= i
        return result

    def taylor(self, x, n):
        import math
        rad = math.radians(x)
        sum_cos = 0
        for i in range(n):
            term = ((-1) ** i) * (rad ** (2 * i)) / self.factorial(2 * i)
            sum_cos += term
        return sum_cos

    def sin(self, x):
        import math
        rad = math.radians(x)
        sum_sin = 0
        term = rad
        i = 1
        while abs(term) > 1e-15:
            sum_sin += term
            term = ((-1) ** i) * (rad ** (2 * i + 1)) / self.factorial(2 * i + 1)
            i += 1
        return round(sum_sin, 10)

    def tan(self, x):
        cos_val = self.cos(x)
        if cos_val == 0:
            return False
        return self.sin(x) / cos_val

import unittest

class TriCalculatorTestSin(unittest.TestCase):
    def test_sin_1(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.sin(30), 0.5)

    def test_sin_2(self):
        tricalculator = TriCalculator()
        self.assertAlmostEqual(tricalculator.sin(60), 0.8660254038)

    def test_sin_3(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.sin(0), 0.0)

    def test_sin_4(self):
        tricalculator = TriCalculator()
        self.assertEqual(tricalculator.sin(90), 1.0)

    def test_sin_5(self):
        tricalculator = TriCalculator()
        self.assertAlmostEqual(tricalculator.sin(45), 0.7071067812)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
