class PersonRequest:
    def __init__(self, name, sex, phone_number):
        self.name = self._validate_name(name)
        self.sex = self._validate_sex(sex)
        self.phone_number = self._validate_phone_number(phone_number)

    def _validate_name(self, name):
        if name and len(name) <= 33:
            return name
        return None

    def _validate_sex(self, sex):
        if sex in ("Man", "Woman", "UGM"):
            return sex
        return None

    def _validate_phone_number(self, phone_number):
        if phone_number and len(phone_number) == 11 and phone_number.isdigit():
            return phone_number
        return None

import unittest

class PersonRequestTestValidateName(unittest.TestCase):
    def test_validate_name_1(self):
        pr = PersonRequest("", "Man", "12345678901")
        self.assertIsNone(pr.name)

    def test_validate_name_2(self):
        pr = PersonRequest("This is a very long name that exceeds the character limit", "Man",
                           "12345678901")
        self.assertIsNone(pr.name)

    def test_validate_name_3(self):
        pr = PersonRequest("aaa", "Man", "12345678901")
        self.assertEqual(pr.name, 'aaa')

    def test_validate_name_4(self):
        pr = PersonRequest("bbb", "Man", "12345678901")
        self.assertEqual(pr.name, 'bbb')

    def test_validate_name_5(self):
        pr = PersonRequest("ccc", "Man", "12345678901")
        self.assertEqual(pr.name, 'ccc')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
