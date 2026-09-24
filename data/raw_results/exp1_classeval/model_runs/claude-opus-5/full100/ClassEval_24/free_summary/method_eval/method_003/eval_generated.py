class ComplexCalculator:
    def __init__(self):
        pass

    @staticmethod
    def add(c1: complex, c2: complex) -> complex:
        real = c1.real + c2.real
        imag = c1.imag + c2.imag
        return complex(real, imag)

    @staticmethod
    def subtract(c1: complex, c2: complex) -> complex:
        real = c1.real - c2.real
        imag = c1.imag - c2.imag
        return complex(real, imag)

    @staticmethod
    def multiply(c1: complex, c2: complex) -> complex:
        a, b = c1.real, c1.imag
        c, d = c2.real, c2.imag
        real = (a * c) - (b * d)
        imag = (a * d) + (b * c)
        return complex(real, imag)

    @staticmethod
    def divide(c1: complex, c2: complex) -> complex:
        a, b = c1.real, c1.imag
        c, d = c2.real, c2.imag
        denominator = (c * c) + (d * d)
        real = (a * c + b * d) / denominator
        imag = (b * c - a * d) / denominator
        return complex(real, imag)

import unittest

class ComplexCalculatorTestDivide(unittest.TestCase):
    def test_divide(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.divide(1+2j, 3+4j), (0.44+0.08j))

    def test_divide_2(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.divide(-1-2j, -3-4j), (0.44+0.08j))

    def test_divide_3(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.divide(1-2j, 3-4j), (0.44-0.08j))

    def test_divide_4(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.divide(-1+2j, -3+4j), (0.44-0.08j))

    def test_divide_5(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.divide(1+2j, -1-2j), (-1+0j))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
