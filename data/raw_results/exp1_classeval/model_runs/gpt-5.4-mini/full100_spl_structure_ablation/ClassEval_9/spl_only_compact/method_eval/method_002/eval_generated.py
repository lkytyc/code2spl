class BigNumCalculator:
    def add(self, num1: str, num2: str) -> str:
        max_length = max(len(num1), len(num2))
        num1 = num1.zfill(max_length)
        num2 = num2.zfill(max_length)

        carry = 0
        result = []

        for i in range(max_length - 1, -1, -1):
            digit_sum = int(num1[i]) + int(num2[i]) + carry
            carry = digit_sum // 10
            digit = digit_sum % 10
            result.insert(0, str(digit))

        if carry > 0:
            result.insert(0, str(carry))

        return "".join(result)

    def multiply(self, num1: str, num2: str) -> str:
        len1, len2 = len(num1), len(num2)
        result = [0] * (len1 + len2)

        for i in range(len1 - 1, -1, -1):
            for j in range(len2 - 1, -1, -1):
                product = int(num1[i]) * int(num2[j])
                p1 = i + j
                p2 = i + j + 1
                total = product + result[p2]
                result[p2] = total % 10
                result[p1] += total // 10

        start = 0
        while start < len(result) - 1 and result[start] == 0:
            start += 1

        final_product_string = "".join(str(x) for x in result[start:])
        return final_product_string

    def subtract(self, num1: str, num2: str) -> str:
        negative = False

        if len(num1) < len(num2):
            num1, num2 = num2, num1
            negative = True
        elif len(num1) > len(num2):
            negative = False
        else:
            if num1 < num2:
                num1, num2 = num2, num1
                negative = True
            else:
                negative = False

        max_length = max(len(num1), len(num2))
        num1 = num1.zfill(max_length)
        num2 = num2.zfill(max_length)

        borrow = 0
        result = []

        for i in range(max_length - 1, -1, -1):
            digit_diff = int(num1[i]) - int(num2[i]) - borrow
            if digit_diff < 0:
                digit_diff += 10
                borrow = 1
            else:
                borrow = 0
            result.insert(0, str(digit_diff))

        while len(result) > 1 and result[0] == '0':
            result.pop(0)

        if negative:
            result.insert(0, '-')

        return "".join(result)

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
