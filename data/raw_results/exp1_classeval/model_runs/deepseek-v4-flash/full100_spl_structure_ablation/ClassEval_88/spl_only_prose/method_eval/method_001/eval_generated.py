class TriCalculator:
    def __init__(self):
        pass

    def cos(self, x):
        taylor_result = self.taylor(x, 50)
        rounded_result = round(taylor_result, 10)
        return rounded_result

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
        while abs(t) >= 1e-15:
            g += t
            n += 1
            t = -t * x * x / (2 * n - 1) / (2 * n - 2)
        return round(g, 10)

    def tan(self, x):
        cos_x = self.cos(x)
        if cos_x != 0:
            result = self.sin(x) / self.cos(x)
            return round(result, 10)
        return False

    def taylor(self, x, n):
        import math
        a = 1
        x = (x / 180) * math.pi
        count = 1
        for k in range(1, n):
            if count % 2 == 1:
                a -= (x ** (2 * k)) / self.factorial(2 * k)
            else:
                a += (x ** (2 * k)) / self.factorial(2 * k)
            count += 1
        return a

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
