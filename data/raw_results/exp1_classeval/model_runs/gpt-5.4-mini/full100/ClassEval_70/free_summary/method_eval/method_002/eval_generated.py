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
