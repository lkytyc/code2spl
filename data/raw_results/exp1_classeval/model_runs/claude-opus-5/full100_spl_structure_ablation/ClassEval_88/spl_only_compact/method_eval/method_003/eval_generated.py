from math import pi, fabs


class TriCalculator:

    def __init__(self):
        pass

    def cos(self) -> float:
        raw_approximation = self.taylor(x, 50)
        rounded_result = round(raw_approximation, 10)
        return rounded_result

    def factorial(self, a: int) -> int:
        b = 1
        while a != 1:
            b = b * a
            a = a - 1
        return b

    def sin(self, x: float) -> float:
        x = (x / 180) * pi
        g = 0
        t = x
        n = 1
        while fabs(t) >= 1e-15:
            g = g + t
            n = n + 1
            t = -t * x * x / (2 * n - 1) / (2 * n - 2)
        return round(g, 10)

    def tan(self, x: float):
        cos_nonzero_check = self.cos(x) != 0
        if cos_nonzero_check:
            raw_tangent = self.sin(x) / self.cos(x)
            rounded_tangent = round(raw_tangent, 10)
            return rounded_tangent
        else:
            return False

    def taylor(self, x, n: int) -> float:
        a = 1
        x = (x / 180) * pi
        count = 1
        for k in range(1, n):
            parity_check = count % 2 != 0
            if parity_check:
                a = a - x ** (2 * k) / self.factorial(2 * k)
            else:
                a = a + x ** (2 * k) / self.factorial(2 * k)
            count = count + 1
        return a

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
