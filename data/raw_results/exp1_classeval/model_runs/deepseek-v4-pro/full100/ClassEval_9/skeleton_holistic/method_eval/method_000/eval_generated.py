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
        num1 = num1.lstrip('0') or '0'
        num2 = num2.lstrip('0') or '0'
        if num1 == '0':
            return num2
        if num2 == '0':
            return num1

        max_len = max(len(num1), len(num2))
        num1 = num1.zfill(max_len)
        num2 = num2.zfill(max_len)

        carry = 0
        result = []
        for i in range(max_len - 1, -1, -1):
            digit_sum = int(num1[i]) + int(num2[i]) + carry
            carry = digit_sum // 10
            result.append(str(digit_sum % 10))
        if carry:
            result.append(str(carry))
        return ''.join(reversed(result))

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
        num1 = num1.lstrip('0') or '0'
        num2 = num2.lstrip('0') or '0'
        if num1 == num2:
            return '0'

        negative = False
        if len(num1) < len(num2) or (len(num1) == len(num2) and num1 < num2):
            num1, num2 = num2, num1
            negative = True

        max_len = max(len(num1), len(num2))
        num1 = num1.zfill(max_len)
        num2 = num2.zfill(max_len)

        borrow = 0
        result = []
        for i in range(max_len - 1, -1, -1):
            diff = int(num1[i]) - int(num2[i]) - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            result.append(str(diff))

        while len(result) > 1 and result[-1] == '0':
            result.pop()
        result_str = ''.join(reversed(result))
        if negative:
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
        num1 = num1.lstrip('0') or '0'
        num2 = num2.lstrip('0') or '0'
        if num1 == '0' or num2 == '0':
            return '0'

        result = [0] * (len(num1) + len(num2))
        num1 = num1[::-1]
        num2 = num2[::-1]

        for i in range(len(num1)):
            carry = 0
            digit1 = int(num1[i])
            for j in range(len(num2)):
                digit2 = int(num2[j])
                product = digit1 * digit2 + result[i + j] + carry
                carry = product // 10
                result[i + j] = product % 10
            if carry:
                result[i + len(num2)] += carry

        while len(result) > 1 and result[-1] == 0:
            result.pop()
        return ''.join(map(str, reversed(result)))

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
