class ComplexCalculator:
    def __init__(self):
        pass

    def add(self, c1: complex, c2: complex) -> complex:
        real = c1.real + c2.real
        imaginary = c1.imag + c2.imag
        answer = complex(real, imaginary)
        return answer

    def divide(self, c1: complex, c2: complex) -> complex:
        denominator = c2.real**2 + c2.imag**2
        if denominator == 0:
            raise ZeroDivisionError("Division by zero in complex division.")
        real = (c1.real * c2.real + c1.imag * c2.imag) / denominator
        imaginary = (c1.imag * c2.real - c1.real * c2.imag) / denominator
        quotient = complex(real, imaginary)
        return quotient

    def multiply(self, c1: complex, c2: complex) -> complex:
        real = c1.real * c2.real - c1.imag * c2.imag
        imaginary = c1.real * c2.imag + c1.imag * c2.real
        result = complex(real, imaginary)
        return result

    def subtract(self, c1: complex, c2: complex) -> complex:
        real = c1.real - c2.real
        imaginary = c1.imag - c2.imag
        result = complex(real, imaginary)
        return result

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
