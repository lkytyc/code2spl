class Chat:
    def __init__(self):
        self.users = {}

    def add_user(self, username):
        if username in self.users:
            return False
        self.users[username] = []
        return True

    def get_messages(self, username):
        if username in self.users:
            return self.users[username]
        return []

    def remove_user(self, username):
        if username in self.users:
            del self.users[username]
            return True
        return False

    def send_message(self, sender, receiver, message):
        if sender not in self.users or receiver not in self.users:
            return False

        from datetime import datetime

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_info = {
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "timestamp": timestamp,
        }

        self.users[sender].append(message_info)
        self.users[receiver].append(message_info)
        return True

import unittest

class ChatTestGetMessages(unittest.TestCase):
    def test_get_messages(self):
        chat = Chat()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat.users = {'John': [{'sender': 'John', 'receiver': 'Mary', 'message': 'Hello', 'timestamp': timestamp}]}
        self.assertEqual(chat.get_messages('John'), [{'sender': 'John', 'receiver': 'Mary', 'message': 'Hello', 'timestamp': timestamp}])

    def test_get_messages_2(self):
        chat = Chat()
        chat.users = {'John': [], 'Mary': []}
        self.assertEqual(chat.get_messages('John'), [])

    def test_get_messages_3(self):
        chat = Chat()
        chat.users = {'John': [], 'Mary': []}
        self.assertEqual(chat.get_messages('Amy'), [])

    def test_get_messages_4(self):
        chat = Chat()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat.users = {'John': [{'sender': 'John', 'receiver': 'Mary', 'message': 'Hello', 'timestamp': timestamp}]}
        self.assertEqual(chat.get_messages('Mary'), [])

    def test_get_messages_5(self):
        chat = Chat()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat.users = {'John': [{'sender': 'John', 'receiver': 'Mary', 'message': 'Hello', 'timestamp': timestamp}]}
        self.assertEqual(chat.get_messages('Amy'), [])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
