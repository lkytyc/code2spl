class BigNumCalculator:
    @staticmethod
    def add(num1, num2):
        i, j = len(num1) - 1, len(num2) - 1
        carry = 0
        res = []
        while i >= 0 or j >= 0 or carry:
            d1 = int(num1[i]) if i >= 0 else 0
            d2 = int(num2[j]) if j >= 0 else 0
            total = d1 + d2 + carry
            carry = total // 10
            res.append(str(total % 10))
            i -= 1
            j -= 1
        return ''.join(reversed(res))

    @staticmethod
    def subtract(num1, num2):
        negative = False
        if len(num1) < len(num2) or (len(num1) == len(num2) and num1 < num2):
            num1, num2 = num2, num1
            negative = True
        i, j = len(num1) - 1, len(num2) - 1
        borrow = 0
        res = []
        while i >= 0:
            d1 = int(num1[i]) - borrow
            d2 = int(num2[j]) if j >= 0 else 0
            if d1 < d2:
                d1 += 10
                borrow = 1
            else:
                borrow = 0
            res.append(str(d1 - d2))
            i -= 1
            j -= 1
        while len(res) > 1 and res[-1] == '0':
            res.pop()
        result = ''.join(reversed(res))
        if negative and result != '0':
            result = '-' + result
        return result

    @staticmethod
    def multiply(num1, num2):
        if num1 == '0' or num2 == '0':
            return '0'
        m, n = len(num1), len(num2)
        result = [0] * (m + n)
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                mul = int(num1[i]) * int(num2[j])
                p1, p2 = i + j, i + j + 1
                total = mul + result[p2]
                result[p2] = total % 10
                result[p1] += total // 10
        start = 0
        while start < len(result) - 1 and result[start] == 0:
            start += 1
        return ''.join(map(str, result[start:]))

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
