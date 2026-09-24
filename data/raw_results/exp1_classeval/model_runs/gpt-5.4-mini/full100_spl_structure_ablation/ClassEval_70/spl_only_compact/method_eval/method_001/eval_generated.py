class PersonRequest:
    def __init__(self, name: str, sex: str, phoneNumber: str):
        self.name = self._validate_name(name)
        self.sex = self._validate_sex(sex)
        self.phoneNumber = self._validate_phoneNumber(phoneNumber)

    def _validate_name(self, name: str):
        if not name:
            return None
        if len(name) > 33:
            return None
        return name

    def _validate_phoneNumber(self, phoneNumber: str):
        if not phoneNumber:
            return None
        if len(phoneNumber) != 11 or not phoneNumber.isdigit():
            return None
        return phoneNumber

    def _validate_sex(self, sex: str):
        if sex not in ("Man", "Woman", "UGM"):
            return None
        return sex

import unittest

class PersonRequestTestValidateSex(unittest.TestCase):
    def test_validate_sex_1(self):
        pr = PersonRequest("John Doe", "Unknown", "12345678901")
        self.assertIsNone(pr.sex)

    def test_validate_sex_2(self):
        pr = PersonRequest("John Doe", "UGM", "12345678901")
        self.assertEqual(pr.sex, "UGM")

    def test_validate_sex_3(self):
        pr = PersonRequest("John Doe", "Man", "12345678901")
        self.assertEqual(pr.sex, "Man")

    def test_validate_sex_4(self):
        pr = PersonRequest("John Doe", "Woman", "12345678901")
        self.assertEqual(pr.sex, "Woman")

    def test_validate_sex_5(self):
        pr = PersonRequest("John Doe", "khsigy", "12345678901")
        self.assertIsNone(pr.sex)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
