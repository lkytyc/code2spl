class BigNumCalculator:
    """
    This is a class that implements big number calculations, including adding, subtracting and multiplying.
    """

    @staticmethod
    def add(num1, num2):
        """
        Adds two big numbers.
        :param num1: The first number to add,str.
        :param num2: The second number to add,str.
        :return: The sum of the two numbers,str.
        >>> bigNum = BigNumCalculator()
        >>> bigNum.add("12345678901234567890", "98765432109876543210")
        '111111111011111111100'

        """
        # Handle signs
        negative = False
        if num1.startswith('-') and num2.startswith('-'):
            negative = True
            num1 = num1[1:]
            num2 = num2[1:]
        elif num1.startswith('-'):
            return BigNumCalculator.subtract(num2, num1[1:])
        elif num2.startswith('-'):
            return BigNumCalculator.subtract(num1, num2[1:])
        
        # Make num1 the longer one
        if len(num1) < len(num2):
            num1, num2 = num2, num1
        
        # Pad num2 with leading zeros
        num2 = num2.zfill(len(num1))
        
        result = []
        carry = 0
        for i in range(len(num1) - 1, -1, -1):
            digit_sum = int(num1[i]) + int(num2[i]) + carry
            result.append(str(digit_sum % 10))
            carry = digit_sum // 10
        
        if carry:
            result.append(str(carry))
        
        result_str = ''.join(reversed(result))
        if negative:
            result_str = '-' + result_str
        return result_str

    @staticmethod
    def subtract(num1, num2):
        """
        Subtracts two big numbers.
        :param num1: The first number to subtract,str.
        :param num2: The second number to subtract,str.
        :return: The difference of the two numbers,str.
        >>> bigNum = BigNumCalculator()
        >>> bigNum.subtract("12345678901234567890", "98765432109876543210")
        '-86419753208641975320'

        """
        # Handle signs
        if num1.startswith('-') and num2.startswith('-'):
            return BigNumCalculator.subtract(num2[1:], num1[1:])
        elif num1.startswith('-'):
            return '-' + BigNumCalculator.add(num1[1:], num2)
        elif num2.startswith('-'):
            return BigNumCalculator.add(num1, num2[1:])
        
        # Determine sign of result
        negative = False
        if len(num1) < len(num2) or (len(num1) == len(num2) and num1 < num2):
            num1, num2 = num2, num1
            negative = True
        
        # Pad num2 with leading zeros
        num2 = num2.zfill(len(num1))
        
        result = []
        borrow = 0
        for i in range(len(num1) - 1, -1, -1):
            digit1 = int(num1[i]) - borrow
            digit2 = int(num2[i])
            if digit1 < digit2:
                digit1 += 10
                borrow = 1
            else:
                borrow = 0
            result.append(str(digit1 - digit2))
        
        # Remove leading zeros
        result_str = ''.join(reversed(result)).lstrip('0')
        if not result_str:
            result_str = '0'
        elif negative:
            result_str = '-' + result_str
        return result_str

    @staticmethod
    def multiply(num1, num2):
        """
        Multiplies two big numbers.
        :param num1: The first number to multiply,str.
        :param num2: The second number to multiply,str.
        :return: The product of the two numbers,str.
        >>> bigNum = BigNumCalculator()
        >>> bigNum.multiply("12345678901234567890", "98765432109876543210")
        '1219326311370217952237463801111263526900'

        """
        # Handle signs
        negative = False
        if num1.startswith('-') and num2.startswith('-'):
            num1 = num1[1:]
            num2 = num2[1:]
        elif num1.startswith('-'):
            negative = True
            num1 = num1[1:]
        elif num2.startswith('-'):
            negative = True
            num2 = num2[1:]
        
        # Make num1 the shorter one for efficiency
        if len(num1) > len(num2):
            num1, num2 = num2, num1
        
        result = [0] * (len(num1) + len(num2))
        
        for i in range(len(num1) - 1, -1, -1):
            carry = 0
            for j in range(len(num2) - 1, -1, -1):
                product = int(num1[i]) * int(num2[j]) + result[i + j + 1] + carry
                result[i + j + 1] = product % 10
                carry = product // 10
            result[i] += carry
        
        # Convert to string and remove leading zeros
        result_str = ''.join(map(str, result)).lstrip('0')
        if not result_str:
            result_str = '0'
        elif negative:
            result_str = '-' + result_str
        return result_str

import unittest

class BigNumCalculatorTestAdd(unittest.TestCase):
    def test_add(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.add("12345678901234567890", "98765432109876543210"), "111111111011111111100")

    def test_add_2(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.add("123456789012345678922", "98765432109876543210"), "222222221122222222132")

    def test_add_3(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.add("123456789012345678934", "98765432109876543210"), "222222221122222222144")

    def test_add_4(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.add("123456789012345678946", "98765432109876543210"), "222222221122222222156")

    def test_add_5(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.add("123456789012345678958", "98765432109876543210"), "222222221122222222168")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
