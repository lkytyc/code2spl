class SignInSystem:
    def __init__(self):
        self.users = {}

    def add_user(self, username):
        if username in self.users:
            return False
        else:
            self.users[username] = False
            return True

    def sign_in(self, username):
        if username not in self.users:
            return False
        else:
            self.users[username] = True
            return True

    def check_sign_in(self, username):
        if username not in self.users:
            return False
        else:
            if self.users[username]:
                return True
            else:
                return False

    def all_signed_in(self):
        if all(self.users.values()):
            return True
        else:
            return False

    def all_not_signed_in(self):
        not_signed_in_users = []
        for username, signed_in in self.users.items():
            if not signed_in:
                not_signed_in_users.append(username)
        return not_signed_in_users

import unittest

class SignInSystemTestAllNotSignedIn(unittest.TestCase):
    def test_all_not_signed_in_1(self):
        signin_system = SignInSystem()
        signin_system.add_user("user1")
        signin_system.sign_in("user1")
        result = signin_system.all_not_signed_in()
        self.assertEqual([], result)

    def test_all_not_signed_in_2(self):
        signin_system = SignInSystem()
        signin_system.add_user("user1")
        signin_system.add_user("user2")
        result = signin_system.all_not_signed_in()
        self.assertEqual(["user1", "user2"], result)

    def test_all_not_signed_in_3(self):
        signin_system = SignInSystem()
        signin_system.add_user("aaa")
        signin_system.sign_in("aaa")
        result = signin_system.all_not_signed_in()
        self.assertEqual([], result)

    def test_all_not_signed_in_4(self):
        signin_system = SignInSystem()
        signin_system.add_user("user1")
        signin_system.add_user("aaa")
        signin_system.sign_in("user1")
        result = signin_system.all_not_signed_in()
        self.assertEqual(['aaa'], result)

    def test_all_not_signed_in_5(self):
        signin_system = SignInSystem()
        result = signin_system.all_not_signed_in()
        self.assertEqual([], result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
