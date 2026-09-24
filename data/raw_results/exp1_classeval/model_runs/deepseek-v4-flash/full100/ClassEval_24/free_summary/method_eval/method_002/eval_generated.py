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
