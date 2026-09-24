class TriCalculator:
    def __init__(self):
        pass

    def factorial(self, a):
        result = 1
        for i in range(2, a + 1):
            result *= i
        return result

    def taylor(self, x, n):
        import math
        rad = math.radians(x)
        total = 1.0
        for i in range(1, n):
            power = 2 * i
            term = (rad ** power) / self.factorial(power)
            if i % 2 == 1:
                total -= term
            else:
                total += term
        return total

    def cos(self, x):
        return round(self.taylor(x, 50), 10)

    def sin(self, x):
        import math
        rad = math.radians(x)
        term = rad
        total = term
        i = 1
        while abs(term) >= 1e-15:
            term *= -rad * rad / ((2 * i) * (2 * i + 1))
            total += term
            i += 1
        return round(total, 10)

    def tan(self, x):
        c = self.cos(x)
        if c == 0:
            return False
        return round(self.sin(x) / c, 10)

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
