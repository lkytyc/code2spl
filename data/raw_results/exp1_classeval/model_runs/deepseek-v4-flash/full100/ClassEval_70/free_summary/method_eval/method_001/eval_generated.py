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
