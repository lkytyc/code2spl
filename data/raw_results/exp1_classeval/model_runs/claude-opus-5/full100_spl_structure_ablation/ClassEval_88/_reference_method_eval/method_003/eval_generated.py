from math import pi, fabs


class TriCalculator:

    def __init__(self):
        pass

    def cos(self, x):
        return round(self.taylor(x, 50), 10)

    def factorial(self, a):
        b = 1
        while a != 1:
            b *= a
            a -= 1
        return b

    def taylor(self, x, n):
        a = 1
        x = x / 180 * pi
        count = 1
        for k in range(1, n):
            if count % 2 != 0:
                a -= (x ** (2 * k)) / self.factorial(2 * k)
            else:
                a += (x ** (2 * k)) / self.factorial(2 * k)
            count += 1
        return a

    def sin(self, x):
        x = x / 180 * pi
        g = 0
        t = x
        n = 1

        while fabs(t) >= 1e-15:
            g += t
            n += 1
            t = -t * x * x / (2 * n - 1) / (2 * n - 2)
        return round(g, 10)

    def tan(self, x):
        if self.cos(x) != 0:
            result = self.sin(x) / self.cos(x)
            return round(result, 10)
        else:
            return False

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
