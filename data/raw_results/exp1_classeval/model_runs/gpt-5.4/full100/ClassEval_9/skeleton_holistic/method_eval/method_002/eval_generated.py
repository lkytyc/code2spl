class BigNumCalculator:
    """
    This is a class that implements big number calculations, including adding, subtracting and multiplying.
    """

    @staticmethod
    def _normalize(num):
        if not isinstance(num, str):
            num = str(num)
        num = num.strip()
        if not num:
            return "0"

        sign = 1
        if num[0] == "-":
            sign = -1
            num = num[1:]
        elif num[0] == "+":
            num = num[1:]

        num = num.lstrip("0")
        if num == "":
            return "0"
        return ("-" if sign < 0 else "") + num

    @staticmethod
    def _compare_abs(num1, num2):
        num1 = num1.lstrip("0") or "0"
        num2 = num2.lstrip("0") or "0"
        if len(num1) > len(num2):
            return 1
        if len(num1) < len(num2):
            return -1
        if num1 > num2:
            return 1
        if num1 < num2:
            return -1
        return 0

    @staticmethod
    def _add_abs(num1, num2):
        i = len(num1) - 1
        j = len(num2) - 1
        carry = 0
        result = []

        while i >= 0 or j >= 0 or carry:
            d1 = ord(num1[i]) - ord("0") if i >= 0 else 0
            d2 = ord(num2[j]) - ord("0") if j >= 0 else 0
            total = d1 + d2 + carry
            result.append(chr(total % 10 + ord("0")))
            carry = total // 10
            i -= 1
            j -= 1

        return "".join(reversed(result))

    @staticmethod
    def _subtract_abs(num1, num2):
        i = len(num1) - 1
        j = len(num2) - 1
        borrow = 0
        result = []

        while i >= 0:
            d1 = ord(num1[i]) - ord("0") - borrow
            d2 = ord(num2[j]) - ord("0") if j >= 0 else 0

            if d1 < d2:
                d1 += 10
                borrow = 1
            else:
                borrow = 0

            result.append(chr(d1 - d2 + ord("0")))
            i -= 1
            j -= 1

        res = "".join(reversed(result)).lstrip("0")
        return res if res else "0"

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
        num1 = BigNumCalculator._normalize(num1)
        num2 = BigNumCalculator._normalize(num2)

        sign1 = -1 if num1.startswith("-") else 1
        sign2 = -1 if num2.startswith("-") else 1
        abs1 = num1[1:] if sign1 == -1 else num1
        abs2 = num2[1:] if sign2 == -1 else num2

        if sign1 == sign2:
            result = BigNumCalculator._add_abs(abs1, abs2)
            return result if sign1 > 0 or result == "0" else "-" + result

        cmp_result = BigNumCalculator._compare_abs(abs1, abs2)
        if cmp_result == 0:
            return "0"
        if cmp_result > 0:
            result = BigNumCalculator._subtract_abs(abs1, abs2)
            return result if sign1 > 0 or result == "0" else "-" + result
        result = BigNumCalculator._subtract_abs(abs2, abs1)
        return result if sign2 > 0 or result == "0" else "-" + result

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
        num2 = BigNumCalculator._normalize(num2)
        if num2 == "0":
            neg_num2 = "0"
        elif num2.startswith("-"):
            neg_num2 = num2[1:]
        else:
            neg_num2 = "-" + num2
        return BigNumCalculator.add(num1, neg_num2)

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
        num1 = BigNumCalculator._normalize(num1)
        num2 = BigNumCalculator._normalize(num2)

        sign1 = -1 if num1.startswith("-") else 1
        sign2 = -1 if num2.startswith("-") else 1
        abs1 = num1[1:] if sign1 == -1 else num1
        abs2 = num2[1:] if sign2 == -1 else num2

        if abs1 == "0" or abs2 == "0":
            return "0"

        result = [0] * (len(abs1) + len(abs2))

        for i in range(len(abs1) - 1, -1, -1):
            for j in range(len(abs2) - 1, -1, -1):
                mul = (ord(abs1[i]) - ord("0")) * (ord(abs2[j]) - ord("0"))
                p1 = i + j
                p2 = i + j + 1

                total = mul + result[p2]
                result[p2] = total % 10
                result[p1] += total // 10

        k = 0
        while k < len(result) and result[k] == 0:
            k += 1

        product = "".join(str(d) for d in result[k:])
        if sign1 * sign2 < 0:
            return "-" + product
        return product

import unittest

class BigNumCalculatorTestMultiply(unittest.TestCase):
    def test_multiply(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.multiply("12345678901234567890", "98765432109876543210"), "1219326311370217952237463801111263526900")

    def test_multiply_2(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.multiply("123456789012345678922", "98765432109876543210"), "12193263113702179524547477517529919219620")

    def test_multiply_3(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.multiply("123456789012345678934", "98765432109876543"), "12193263113702179499806737010255845162")

    def test_multiply_4(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.multiply("12345678901234567", "98765432109876543210"), "1219326311370217864336229223321140070")

    def test_multiply_5(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.multiply("923456789", "187654321"), "173290656712635269")

    def test_multiply_6(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.multiply("000000001", "000000001"), "1")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
