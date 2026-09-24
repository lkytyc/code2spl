class PersonRequest:
    def __init__(self, name, sex, phone):
        self.name = self._validate_name(name)
        self.sex = self._validate_sex(sex)
        self.phone = self._validate_phone(phone)

    def _validate_name(self, name):
        if isinstance(name, str) and 0 < len(name) <= 33:
            return name
        return None

    def _validate_sex(self, sex):
        if sex in ("Man", "Woman", "UGM"):
            return sex
        return None

    def _validate_phone(self, phone):
        if isinstance(phone, str) and len(phone) == 11 and phone.isdigit():
            return phone
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
