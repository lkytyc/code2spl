class SignInSystem:
    def __init__(self):
        self.users = {}

    def add_user(self, username):
        if username in self.users:
            return False
        self.users[username] = False
        return True

    def sign_in(self, username):
        if username not in self.users:
            return False
        self.users[username] = True
        return True

    def check_sign_in(self, username):
        return username in self.users and self.users[username] is True

    def all_signed_in(self):
        return all(self.users.values())

    def all_not_signed_in(self):
        return [username for username, signed_in in self.users.items() if not signed_in]

import unittest

class SignInSystemTestAllSignedIn(unittest.TestCase):
    def test_all_signed_in_1(self):
        signin_system = SignInSystem()
        signin_system.add_user("user1")
        signin_system.sign_in("user1")
        result = signin_system.all_signed_in()
        self.assertTrue(result)

    def test_all_signed_in_2(self):
        signin_system = SignInSystem()
        signin_system.add_user("user1")
        result = signin_system.all_signed_in()
        self.assertFalse(result)

    def test_all_signed_in_3(self):
        signin_system = SignInSystem()
        signin_system.add_user("aaa")
        signin_system.sign_in("aaa")
        result = signin_system.all_signed_in()
        self.assertTrue(result)

    def test_all_signed_in_4(self):
        signin_system = SignInSystem()
        signin_system.add_user("bbb")
        signin_system.sign_in("bbb")
        result = signin_system.all_signed_in()
        self.assertTrue(result)

    def test_all_signed_in_5(self):
        signin_system = SignInSystem()
        signin_system.add_user("aaa")
        signin_system.add_user("bbb")
        signin_system.sign_in("aaa")
        result = signin_system.all_signed_in()
        self.assertFalse(result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
