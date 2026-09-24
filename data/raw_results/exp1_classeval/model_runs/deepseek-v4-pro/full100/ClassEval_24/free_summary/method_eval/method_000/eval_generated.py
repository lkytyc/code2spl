class ComplexCalculator:
    @staticmethod
    def add(c1, c2):
        return c1 + c2

    @staticmethod
    def subtract(c1, c2):
        return c1 - c2

    @staticmethod
    def multiply(c1, c2):
        real = c1.real * c2.real - c1.imag * c2.imag
        imag = c1.real * c2.imag + c1.imag * c2.real
        return complex(real, imag)

    @staticmethod
    def divide(c1, c2):
        denominator = c2.real**2 + c2.imag**2
        real = (c1.real * c2.real + c1.imag * c2.imag) / denominator
        imag = (c1.imag * c2.real - c1.real * c2.imag) / denominator
        return complex(real, imag)

import unittest

class ComplexCalculatorTestAdd(unittest.TestCase):
    def test_add(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.add(1+2j, 3+4j), (4+6j))

    def test_add_2(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.add(-1 - 2j, -3 - 4j), (-4 - 6j))

    def test_add_3(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.add(1-2j, 3-4j), (4-6j))

    def test_add_4(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.add(-1+2j, -3+4j), (-4+6j))

    def test_add_5(self):
        complexCalculator = ComplexCalculator()
        self.assertEqual(complexCalculator.add(1+2j, -1-2j), (0+0j))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
