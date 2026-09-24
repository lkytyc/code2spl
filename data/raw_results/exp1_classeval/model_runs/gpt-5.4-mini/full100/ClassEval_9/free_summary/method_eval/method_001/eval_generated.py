class BigNumCalculator:
    @staticmethod
    def add(num1, num2):
        if num1 == "":
            num1 = "0"
        if num2 == "":
            num2 = "0"

        max_len = max(len(num1), len(num2))
        num1 = num1.zfill(max_len)
        num2 = num2.zfill(max_len)

        carry = 0
        result = []

        for i in range(max_len - 1, -1, -1):
            total = int(num1[i]) + int(num2[i]) + carry
            result.append(str(total % 10))
            carry = total // 10

        if carry:
            result.append(str(carry))

        return "".join(reversed(result))

    @staticmethod
    def subtract(num1, num2):
        if num1 == "":
            num1 = "0"
        if num2 == "":
            num2 = "0"

        def normalize(s):
            s = s.lstrip("0")
            return s if s else "0"

        num1 = normalize(num1)
        num2 = normalize(num2)

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

        result_str = "".join(reversed(result)).lstrip("0")
        if result_str == "":
            result_str = "0"

        if negative and result_str != "0":
            result_str = "-" + result_str

        return result_str

    @staticmethod
    def multiply(num1, num2):
        if num1 == "" or num2 == "":
            return "0"

        num1 = num1.lstrip("0") or "0"
        num2 = num2.lstrip("0") or "0"

        if num1 == "0" or num2 == "0":
            return "0"

        len1 = len(num1)
        len2 = len(num2)
        result = [0] * (len1 + len2)

        for i in range(len1 - 1, -1, -1):
            for j in range(len2 - 1, -1, -1):
                product = int(num1[i]) * int(num2[j])
                pos_low = i + j + 1
                pos_high = i + j
                total = product + result[pos_low]
                result[pos_low] = total % 10
                result[pos_high] += total // 10

        idx = 0
        while idx < len(result) - 1 and result[idx] == 0:
            idx += 1

        return "".join(str(d) for d in result[idx:])

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
