from datetime import datetime

class Chat:
    def __init__(self):
        self.users = {}

    def add_user(self, username):
        if username in self.users:
            return False
        self.users[username] = []
        return True

    def remove_user(self, username):
        if username not in self.users:
            return False
        del self.users[username]
        return True

    def send_message(self, sender, receiver, message):
        if sender not in self.users or receiver not in self.users:
            return False

        record = {
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.users[sender].append(record)
        self.users[receiver].append(record)
        return True

    def get_messages(self, username):
        if username not in self.users:
            return []
        return self.users[username]

import unittest

class ChatTestAddUser(unittest.TestCase):
    def test_add_user(self):
        chat = Chat()
        self.assertEqual(chat.add_user('John'), True)
        self.assertEqual(chat.users, {'John': []})
    def test_add_user_2(self):
        chat = Chat()
        chat.users = {'John': []}
        self.assertEqual(chat.add_user('John'), False)
        self.assertEqual(chat.users, {'John': []})

    def test_add_user_3(self):
        chat = Chat()
        chat.users = {'John': []}
        self.assertEqual(chat.add_user('Mary'), True)
        self.assertEqual(chat.users, {'John': [], 'Mary': []})

    def test_add_user_4(self):
        chat = Chat()
        chat.users = {'John': []}
        self.assertEqual(chat.add_user('Mary'), True)
        self.assertEqual(chat.users, {'John': [], 'Mary': []})

    def test_add_user_5(self):
        chat = Chat()
        self.assertEqual(chat.add_user('John'), True)
        self.assertEqual(chat.add_user('Mary'), True)
        self.assertEqual(chat.users, {'John': [], 'Mary': []})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
