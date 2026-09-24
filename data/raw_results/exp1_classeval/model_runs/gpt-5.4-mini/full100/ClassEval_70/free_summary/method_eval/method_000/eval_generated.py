class PersonRequest:
    def __init__(self, name, sex, phoneNumber):
        self.__name = self.__validate_name(name)
        self.__sex = self.__validate_sex(sex)
        self.__phoneNumber = self.__validate_phone_number(phoneNumber)

    def __validate_name(self, name):
        if name is not None and name != "" and len(name) <= 33:
            return name
        return None

    def __validate_sex(self, sex):
        if sex in ("Man", "Woman", "UGM"):
            return sex
        return None

    def __validate_phone_number(self, phoneNumber):
        if phoneNumber is not None and phoneNumber != "" and len(phoneNumber) == 11 and phoneNumber.isdigit():
            return phoneNumber
        return None

    def getName(self):
        return self.__name

    def getSex(self):
        return self.__sex

    def getPhoneNumber(self):
        return self.__phoneNumber

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
