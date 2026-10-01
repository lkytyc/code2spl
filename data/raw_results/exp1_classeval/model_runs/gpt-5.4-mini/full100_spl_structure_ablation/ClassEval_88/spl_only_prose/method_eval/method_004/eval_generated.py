class TriCalculator:
    def __init__(self):
        pass

    def cos(self, x):
        taylor_value = self.taylor(x, 50)
        return round(taylor_value, 10)

    def factorial(self, a):
        b = 1
        while a != 1:
            b *= a
            a -= 1
        return b

    def sin(self, x):
        x = x / 180 * 3.141592653589793
        g = 0
        t = x
        n = 1
        while abs(t) >= 1e-15:
            g += t
            n += 1
            t = -t * x * x / (2 * n - 1) / (2 * n - 2)
        return round(g, 10)

    def tan(self, x):
        condition = self.cos(x) != 0
        if condition:
            result = self.sin(x) / self.cos(x)
            return round(result, 10)
        return False

    def taylor(self, x, n):
        a = 1
        x = x / 180 * 3.141592653589793
        count = 1
        for k in range(1, n):
            term = (x ** (2 * k)) / self.factorial(2 * k)
            if count % 2 == 1:
                a -= term
            else:
                a += term
            count += 1
        return a

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
