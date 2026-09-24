class ComplexCalculator:
    def __init__(self):
        pass

    def add(self, c1: complex, c2: complex) -> complex:
        real = c1.real + c2.real
        imaginary = c1.imag + c2.imag
        answer = complex(real, imaginary)
        return answer

    def divide(self, c1: complex, c2: complex) -> complex:
        denominator = c2.real * c2.real + c2.imag * c2.imag
        real = (c1.real * c2.real + c1.imag * c2.imag) / denominator
        imaginary = (c1.imag * c2.real - c1.real * c2.imag) / denominator
        result = complex(real, imaginary)
        return result

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

class ComplexCalculatorTestSubtract(unittest.TestCase):
    def test_subtract(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.subtract(1+2j, 3+4j), (-2-2j))

    def test_subtract_2(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.subtract(-1-2j, -3-4j), (2+2j))

    def test_subtract_3(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.subtract(1-2j, 3-4j), (-2+2j))

    def test_subtract_4(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.subtract(-1+2j, -3+4j), (2-2j))

    def test_subtract_5(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.subtract(1+2j, 1+2j), (0+0j))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
