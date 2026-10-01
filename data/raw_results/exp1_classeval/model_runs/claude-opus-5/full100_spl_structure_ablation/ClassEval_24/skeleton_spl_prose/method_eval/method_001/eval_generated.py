class ComplexCalculator:
    """
    This is a class that implements addition, subtraction, multiplication, and division operations for complex numbers.
    """

    def __init__(self):
        pass

    @staticmethod
    def add(c1, c2):
        """
        Adds two complex numbers.
        :param c1: The first complex number,complex.
        :param c2: The second complex number,complex.
        :return: The sum of the two complex numbers,complex.
        >>> complexCalculator = ComplexCalculator()
        >>> complexCalculator.add(1+2j, 3+4j)
        (4+6j)

        """
        real = c1.real + c2.real
        imaginary = c1.imag + c2.imag
        answer = complex(real, imaginary)
        return answer

    @staticmethod
    def subtract(c1, c2):
        """
        Subtracts two complex numbers.
        :param c1: The first complex number,complex.
        :param c2: The second complex number,complex.
        :return: The difference of the two complex numbers,complex.
        >>> complexCalculator = ComplexCalculator()
        >>> complexCalculator.subtract(1+2j, 3+4j)
        (-2-2j)

        """
        real = c1.real - c2.real
        imaginary = c1.imag - c2.imag
        return complex(real, imaginary)

    @staticmethod
    def multiply(c1, c2):
        """
        Multiplies two complex numbers.
        :param c1: The first complex number,complex.
        :param c2: The second complex number,complex.
        :return: The product of the two complex numbers,complex.
        >>> complexCalculator = ComplexCalculator()
        >>> complexCalculator.multiply(1+2j, 3+4j)
        (-5+10j)

        """
        real = c1.real * c2.real - c1.imag * c2.imag
        imaginary = c1.real * c2.imag + c1.imag * c2.real
        return complex(real, imaginary)

    @staticmethod
    def divide(c1, c2):
        """
        Divides two complex numbers.
        :param c1: The first complex number,complex.
        :param c2: The second complex number,complex.
        :return: The quotient of the two complex numbers,complex.
        >>> complexCalculator = ComplexCalculator()
        >>> complexCalculator.divide(1+2j, 3+4j)
        (0.44+0.08j)

        """
        denominator = c2.real ** 2 + c2.imag ** 2
        real = (c1.real * c2.real + c1.imag * c2.imag) / denominator
        imaginary = (c1.imag * c2.real - c1.real * c2.imag) / denominator
        return complex(real, imaginary)

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
