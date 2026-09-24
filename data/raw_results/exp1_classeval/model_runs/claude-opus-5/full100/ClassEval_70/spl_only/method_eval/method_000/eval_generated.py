class PersonRequest:
    def __init__(self, name, sex, phoneNumber):
        self.name = self._validate_name(name)
        self.sex = self._validate_sex(sex)
        self.phoneNumber = self._validate_phoneNumber(phoneNumber)

    def _validate_name(self, name):
        if not name:
            return None
        if len(name) > 33:
            return None
        return name

    def _validate_sex(self, sex):
        if sex not in ['Man', 'Woman', 'UGM']:
            return None
        return sex

    def _validate_phoneNumber(self, phoneNumber):
        if not phoneNumber:
            return None
        if len(phoneNumber) != 11 or not phoneNumber.isdigit():
            return None
        return phoneNumber

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
