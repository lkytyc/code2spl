from datetime import datetime


class Chat:
    def __init__(self):
        self.users = {}

    def add_user(self, username: str) -> bool:
        if username not in self.users:
            self.users[username] = []
            return True
        return False

    def get_messages(self, username: str) -> list:
        if username in self.users:
            return self.users[username]
        return []

    def remove_user(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            return True
        return False

    def send_message(self, sender: str, receiver: str, message: str) -> bool:
        if sender in self.users and receiver in self.users:
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
        return False

import unittest

class ChatTestSendMessage(unittest.TestCase):
    def test_send_message(self):
        chat = Chat()
        chat.users = {'John': [], 'Mary': []}
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(chat.send_message('John', 'Mary', 'Hello'), True)
        self.assertEqual(chat.users, {'John': [{'sender': 'John', 'receiver': 'Mary', 'message': 'Hello', 'timestamp': timestamp}], 'Mary': [{'sender': 'John', 'receiver': 'Mary', 'message': 'Hello', 'timestamp': timestamp}]})

    def test_send_message_2(self):
        chat = Chat()
        chat.users = {'John': [], 'Mary': []}
        self.assertEqual(chat.send_message('John', 'Tom', 'Hello'), False)
        self.assertEqual(chat.users, {'John': [], 'Mary': []})

    def test_send_message_3(self):
        chat = Chat()
        chat.users = {'John': [], 'Mary': []}
        self.assertEqual(chat.send_message('Amy', 'Mary', 'Hello'), False)
        self.assertEqual(chat.users, {'John': [], 'Mary': []})

    def test_send_message_4(self):
        chat = Chat()
        chat.users = {'John': [], 'Mary': []}
        self.assertEqual(chat.send_message('Amy', 'Tom', 'Hello'), False)
        self.assertEqual(chat.users, {'John': [], 'Mary': []})

    def test_send_message_5(self):
        chat = Chat()
        chat.users = {'John': [], 'Mary': []}
        self.assertEqual(chat.send_message('Amy', 'Amy', 'Hello'), False)
        self.assertEqual(chat.users, {'John': [], 'Mary': []})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
