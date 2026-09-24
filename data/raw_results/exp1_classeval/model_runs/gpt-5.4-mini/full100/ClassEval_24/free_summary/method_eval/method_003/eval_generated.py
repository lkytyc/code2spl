class ComplexCalculator:
    def __init__(self):
        pass

    @staticmethod
    def add(c1, c2):
        return complex(c1.real + c2.real, c1.imag + c2.imag)

    @staticmethod
    def subtract(c1, c2):
        return complex(c1.real - c2.real, c1.imag - c2.imag)

    @staticmethod
    def multiply(c1, c2):
        return complex(
            c1.real * c2.real - c1.imag * c2.imag,
            c1.real * c2.imag + c1.imag * c2.real,
        )

    @staticmethod
    def divide(c1, c2):
        denominator = c2.real ** 2 + c2.imag ** 2
        return complex(
            (c1.real * c2.real + c1.imag * c2.imag) / denominator,
            (c1.imag * c2.real - c1.real * c2.imag) / denominator,
        )

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
