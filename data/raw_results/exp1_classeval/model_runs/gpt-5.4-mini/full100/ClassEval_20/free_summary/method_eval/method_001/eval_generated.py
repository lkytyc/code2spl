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
        import datetime
        record = {
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "timestamp": datetime.datetime.now(),
        }
        self.users[sender].append(record)
        self.users[receiver].append(record)
        return True

    def get_messages(self, username):
        if username not in self.users:
            return []
        return self.users[username]

import unittest

class ChatTestRemoveUser(unittest.TestCase):
    def test_remove_user(self):
        chat = Chat()
        chat.users = {'John': []}
        self.assertEqual(chat.remove_user('John'), True)
        self.assertEqual(chat.users, {})
    def test_remove_user_2(self):
        chat = Chat()
        self.assertEqual(chat.remove_user('John'), False)
        self.assertEqual(chat.users, {})

    def test_remove_user_3(self):
        chat = Chat()
        chat.users = {'John': [], 'Mary': []}
        self.assertEqual(chat.remove_user('John'), True)
        self.assertEqual(chat.users, {'Mary': []})

    def test_remove_user_4(self):
        chat = Chat()
        chat.users = {'John': [], 'Mary': []}
        self.assertEqual(chat.remove_user('Mary'), True)
        self.assertEqual(chat.remove_user('John'), True)
        self.assertEqual(chat.users, {})

    def test_remove_user_5(self):
        chat = Chat()
        chat.users = {'John': [], 'Mary': []}
        self.assertEqual(chat.remove_user('Amy'), False)
        self.assertEqual(chat.users, {'John': [], 'Mary': []})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
