class ComplexCalculator:
    @staticmethod
    def add(a, b):
        return complex(a.real + b.real, a.imag + b.imag)

    @staticmethod
    def subtract(a, b):
        return complex(a.real - b.real, a.imag - b.imag)

    @staticmethod
    def multiply(a, b):
        real = a.real * b.real - a.imag * b.imag
        imag = a.real * b.imag + a.imag * b.real
        return complex(real, imag)

    @staticmethod
    def divide(a, b):
        denom = b.real * b.real + b.imag * b.imag
        real = (a.real * b.real + a.imag * b.imag) / denom
        imag = (a.imag * b.real - a.real * b.imag) / denom
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
