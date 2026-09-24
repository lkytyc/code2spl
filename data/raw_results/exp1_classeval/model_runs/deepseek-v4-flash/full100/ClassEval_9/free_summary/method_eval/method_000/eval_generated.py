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
