class BigNumCalculator:
    @staticmethod
    def add(a: str, b: str) -> str:
        n = max(len(a), len(b))
        a = a.zfill(n)
        b = b.zfill(n)
        carry = 0
        result = []
        for i in range(n - 1, -1, -1):
            total = int(a[i]) + int(b[i]) + carry
            result.append(str(total % 10))
            carry = total // 10
        if carry:
            result.append(str(carry))
        return ''.join(reversed(result)).lstrip('0') or '0'

    @staticmethod
    def subtract(a: str, b: str) -> str:
        a = a.lstrip('0') or '0'
        b = b.lstrip('0') or '0'
        if len(a) != len(b):
            negative = len(a) < len(b)
        else:
            negative = a < b
        if negative:
            a, b = b, a
        if a == b:
            return '0'
        b = b.zfill(len(a))
        borrow = 0
        result = []
        for i in range(len(a) - 1, -1, -1):
            diff = int(a[i]) - int(b[i]) - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            result.append(str(diff))
        outcome = ''.join(reversed(result)).lstrip('0') or '0'
        if negative and outcome != '0':
            outcome = '-' + outcome
        return outcome

    @staticmethod
    def multiply(a: str, b: str) -> str:
        a = a.lstrip('0') or '0'
        b = b.lstrip('0') or '0'
        if a == '0' or b == '0':
            return '0'
        m, n = len(a), len(b)
        result = [0] * (m + n)
        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                result[i + j + 1] += int(a[i]) * int(b[j])
        for k in range(len(result) - 1, 0, -1):
            result[k - 1] += result[k] // 10
            result[k] %= 10
        s = ''.join(map(str, result))
        return s.lstrip('0') or '0'

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
