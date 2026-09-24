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

class BigNumCalculatorTestSubtract(unittest.TestCase):
    def test_subtract(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.subtract("12345678901234567890", "98765432109876543210"), "-86419753208641975320")

    def test_subtract_2(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.subtract("123456789012345678922", "98765432109876543210"), "24691356902469135712")

    def test_subtract_3(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.subtract("123456789012345678934", "98765432109876543"), "123358023580235802391")

    def test_subtract_4(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.subtract("12345678901234567", "98765432109876543210"), "-98753086430975308643")

    def test_subtract_5(self):
        bigNum = BigNumCalculator()
        self.assertEqual(bigNum.subtract("923456789", "187654321"), "735802468")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
