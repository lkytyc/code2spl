class TriCalculator:
    def __init__(self):
        pass

    def cos(self, x):
        taylor_value = self.taylor(x, 50)
        result = round(taylor_value, 10)
        return result

    def factorial(self, a):
        b = 1
        while a != 1:
            b *= a
            a -= 1
        return b

    def sin(self, x):
        import math

        x = x / 180 * math.pi
        g = 0
        t = x
        n = 1

        while math.fabs(t) >= 1e-15:
            g += t
            n += 1
            t = -t * x * x / (2 * n - 1) / (2 * n - 2)

        return round(g, 10)

    def tan(self, x):
        cos_value = self.cos(x)
        if cos_value != 0:
            result = self.sin(x) / self.cos(x)
            return round(result, 10)
        return False

    def taylor(self, x, n):
        import math

        a = 1
        x = x / 180 * math.pi
        count = 1

        for k in range(1, n):
            parity_check = count % 2 != 0
            if parity_check:
                a -= (x ** (2 * k)) / self.factorial(2 * k)
            else:
                a += (x ** (2 * k)) / self.factorial(2 * k)
            count += 1

        return a

import unittest

class TriCalculatorTestTaylor(unittest.TestCase):
    def test_taylor_1(self):
        tricalculator = TriCalculator()
        self.assertAlmostEqual(tricalculator.taylor(60, 50), 0.5)

    def test_taylor_2(self):
        tricalculator = TriCalculator()
        self.assertAlmostEqual(tricalculator.taylor(30, 50), 0.8660254037844386)

    def test_taylor_3(self):
        tricalculator = TriCalculator()
        self.assertAlmostEqual(tricalculator.taylor(90, 50), 0.0)

    def test_taylor_4(self):
        tricalculator = TriCalculator()
        self.assertAlmostEqual(tricalculator.taylor(0, 50), 1.0)

    def test_taylor_5(self):
        tricalculator = TriCalculator()
        self.assertAlmostEqual(tricalculator.taylor(45, 50), 0.7071067811865475)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
