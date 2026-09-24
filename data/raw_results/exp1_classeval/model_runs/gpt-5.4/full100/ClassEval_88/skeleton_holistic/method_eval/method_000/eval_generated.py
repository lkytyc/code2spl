from math import pi, fabs

class TriCalculator:
    """
    The class allows to calculate trigonometric values, including cosine, sine, and tangent, using Taylor series approximations.
    """

    def __init__(self):
        pass

    def cos(self, x):
        """
        Calculate the cos value of the x-degree angle
        :param x:float
        :return:float
        >>> tricalculator = TriCalculator()
        >>> tricalculator.cos(60)
        0.5
        """
        return self.taylor(x, 50)

    def factorial(self, a):
        """
        Calculate the factorial of a
        :param a: int
        :return: int
        >>> tricalculator.factorial(5)
        120
        """
        if a < 0:
            raise ValueError("factorial() not defined for negative values")
        result = 1
        for i in range(2, int(a) + 1):
            result *= i
        return result

    def taylor(self, x, n):
        """
        Finding the n-order Taylor expansion value of cos (x/180 * pi)
        :param x: int
        :param n: int
        :return: float
        >>> tricalculator.taylor(60, 50)
        0.5000000000000001
        """
        rad = x / 180.0 * pi
        result = 0.0
        for i in range(n):
            result += ((-1) ** i) * (rad ** (2 * i)) / self.factorial(2 * i)
        return result

    def sin(self, x):
        """
        Calculate the sin value of the x-degree angle
        :param x: float
        :return: float
        >>> tricalculator.sin(30)
        0.5
        """
        rad = x / 180.0 * pi
        result = 0.0
        for i in range(50):
            result += ((-1) ** i) * (rad ** (2 * i + 1)) / self.factorial(2 * i + 1)
        return result

    def tan(self, x):
        """
        Calculate the tan value of the x-degree angle
        :param x: float
        :return: float
        >>> tricalculator.tan(45)
        1.0
        """
        cos_val = self.cos(x)
        if fabs(cos_val) < 1e-15:
            raise ZeroDivisionError("tan undefined for this angle")
        return self.sin(x) / cos_val

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
