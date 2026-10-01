class SignInSystem:
    def __init__(self):
        self.users = {}

    def add_user(self, username):
        username_exists = username in self.users
        if username_exists:
            return False
        self.users[username] = False
        return True

    def all_not_signed_in(self):
        not_signed_in_users = []
        for username, signed_in in self.users.items():
            if not signed_in:
                not_signed_in_users.append(username)
        return not_signed_in_users

    def all_signed_in(self):
        condition_result = all(self.users.values())
        if condition_result:
            return True
        return False

    def check_sign_in(self, username):
        if username not in self.users:
            return False
        if self.users[username]:
            return True
        return False

    def sign_in(self, username):
        if username not in self.users:
            return False
        self.users[username] = True
        return True

import unittest

class SignInSystemTestAddUser(unittest.TestCase):
    def test_add_user_1(self):
        signin_system = SignInSystem()
        result = signin_system.add_user("user1")
        self.assertTrue(result)

    def test_add_user_2(self):
        signin_system = SignInSystem()
        signin_system.add_user("user1")
        result = signin_system.add_user("user1")
        self.assertFalse(result)

    def test_add_user_3(self):
        signin_system = SignInSystem()
        result = signin_system.add_user("aaa")
        self.assertTrue(result)

    def test_add_user_4(self):
        signin_system = SignInSystem()
        result = signin_system.add_user("bbb")
        self.assertTrue(result)

    def test_add_user_5(self):
        signin_system = SignInSystem()
        result = signin_system.add_user("ccc")
        self.assertTrue(result)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
