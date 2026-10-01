class ComplexCalculator:
    def __init__(self):
        pass

    def add(self, c1: complex, c2: complex) -> complex:
        real = c1.real + c2.real
        imaginary = c1.imag + c2.imag
        answer = complex(real, imaginary)
        return answer

    def divide(self, c1: complex, c2: complex) -> complex:
        denominator = c2.real ** 2 + c2.imag ** 2
        real = (c1.real * c2.real + c1.imag * c2.imag) / denominator
        imaginary = (c1.imag * c2.real - c1.real * c2.imag) / denominator
        return_value = complex(real, imaginary)
        return return_value

    def multiply(self, c1: complex, c2: complex) -> complex:
        real = c1.real * c2.real - c1.imag * c2.imag
        imaginary = c1.real * c2.imag + c1.imag * c2.real
        result = complex(real, imaginary)
        return result

    def subtract(self, c1: complex, c2: complex) -> complex:
        real = c1.real - c2.real
        imaginary = c1.imag - c2.imag
        return_value = complex(real, imaginary)
        return return_value

import unittest

class ComplexCalculatorTestMultiply(unittest.TestCase):
    def test_multiply(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.multiply(1+2j, 3+4j), (-5+10j))

    def test_multiply_2(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.multiply(-1-2j, -3-4j), (-5+10j))

    def test_multiply_3(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.multiply(1-2j, 3-4j), (-5-10j))

    def test_multiply_4(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.multiply(-1+2j, -3+4j), (-5-10j))

    def test_multiply_5(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.multiply(1+2j, -1-2j), (3-4j))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
