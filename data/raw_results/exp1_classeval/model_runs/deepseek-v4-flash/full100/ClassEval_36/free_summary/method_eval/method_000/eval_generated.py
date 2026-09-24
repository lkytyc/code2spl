import time

class EmailClient:
    def __init__(self, address, capacity):
        self.address = address
        self.capacity = capacity
        self.inbox = []

    def send_to(self, recipient, content, size):
        if not recipient.is_full_with_one_more_email(size):
            email = {
                "sender": self.address,
                "receiver": recipient.address,
                "content": content,
                "size": size,
                "timestamp": time.time(),
                "read": False,
            }
            recipient.inbox.append(email)
            return True
        self.clear_inbox(size)
        return False

    def fetch(self):
        for email in self.inbox:
            if not email["read"]:
                email["read"] = True
                return email
        return None

    def get_occupied_size(self):
        return sum(email["size"] for email in self.inbox)

    def is_full_with_one_more_email(self, size):
        return self.get_occupied_size() + size > self.capacity

    def clear_inbox(self, amount):
        freed = 0
        while freed < amount and self.inbox:
            email = self.inbox.pop(0)
            freed += email["size"]

import unittest

class EmailClientTestSendTo(unittest.TestCase):
    def test_send_to(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertTrue(sender.send_to(receiver, 'Hello', 10))
        self.assertEqual(receiver.inbox[0], {"sender": 'sender@example.com','receiver': 'receiver@example.com','content': 'Hello','size': 10,'time': timestamp,'state': 'unread'})

    def test_send_to_2(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 0)
        self.assertFalse(sender.send_to(receiver, 'Hello', 10))

    def test_send_to_3(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        receiver.inbox = [{'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 50, 'time': '2021-01-01 00:00:00', 'state': 'unread'}]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertFalse(sender.send_to(receiver, 'Hello', 10))
        self.assertEqual(receiver.inbox, [{'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 50, 'time': '2021-01-01 00:00:00', 'state': 'unread'}])

    def test_send_to_4(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 30)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertTrue(sender.send_to(receiver, 'Hello', 20))
        self.assertEqual(receiver.inbox, [{'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 20, 'time': timestamp, 'state': 'unread'}])

    def test_send_to_5(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 30)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertTrue(sender.send_to(receiver, 'bye', 20))
        self.assertEqual(receiver.inbox, [{'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'bye', 'size': 20, 'time': timestamp, 'state': 'unread'}])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
