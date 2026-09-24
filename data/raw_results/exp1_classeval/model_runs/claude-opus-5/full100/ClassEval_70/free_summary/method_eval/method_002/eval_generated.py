class PersonRequest:
    def __init__(self, name: str, sex: str, phoneNumber: str):
        self.name = self._validate_name(name)
        self.sex = self._validate_sex(sex)
        self.phoneNumber = self._validate_phone_number(phoneNumber)

    def _validate_name(self, name: str):
        if name and len(name) <= 33:
            return name
        return None

    def _validate_sex(self, sex: str):
        if sex in ("Man", "Woman", "UGM"):
            return sex
        return None

    def _validate_phone_number(self, phoneNumber: str):
        if phoneNumber and len(phoneNumber) == 11 and phoneNumber.isdigit():
            return phoneNumber
        return None

import unittest

class PersonRequestTestValidatePhoneNumber(unittest.TestCase):
    def test_validate_phoneNumber_1(self):
        pr = PersonRequest("John Doe", "Man", "")
        self.assertIsNone(pr.phoneNumber)

    def test_validate_phoneNumber_2(self):
        pr = PersonRequest("John Doe", "Man", "12345")
        self.assertIsNone(pr.phoneNumber)

    def test_validate_phoneNumber_3(self):
        pr = PersonRequest("John Doe", "Man", "jgdjrj")
        self.assertIsNone(pr.phoneNumber)

    def test_validate_phoneNumber_4(self):
        pr = PersonRequest("John Doe", "Man", "12345678901")
        self.assertEqual(pr.phoneNumber, "12345678901")

    def test_validate_phoneNumber_5(self):
        pr = PersonRequest("John Doe", "Man", "11111111111")
        self.assertEqual(pr.phoneNumber, "11111111111")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
