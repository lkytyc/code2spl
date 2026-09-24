from datetime import datetime


class EmailClient:
    def __init__(self, address, capacity):
        self.address = address
        self.capacity = capacity
        self.inbox = []

    def send_to(self, recv, content, size):
        if not recv.is_full_with_one_more_email(size):
            email = {
                "sender": self.address,
                "receiver": recv.address,
                "content": content,
                "size": size,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "state": "unread",
            }
            recv.inbox.append(email)
            return True
        else:
            self.clear_inbox(size)
            return False

    def fetch(self):
        if not self.inbox:
            return None
        for email in self.inbox:
            if email.get("state") == "unread":
                email["state"] = "read"
                return email
        return None

    def is_full_with_one_more_email(self, size):
        return self.get_occupied_size() + size > self.capacity

    def get_occupied_size(self):
        return sum(email.get("size", 0) for email in self.inbox)

    def clear_inbox(self, size):
        if self.address == "":
            return
        freed = 0
        while self.inbox and freed < size:
            email = self.inbox.pop(0)
            freed += email.get("size", 0)

import unittest

class EmailClientTestFetch(unittest.TestCase):
    def test_fetch(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        receiver.inbox = [
            {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 10,
             'time': timestamp, 'state': 'unread'}]
        self.assertEqual(receiver.fetch(), {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 10, 'time':timestamp, 'state': 'read'})

    def test_fetch_2(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(receiver.fetch(),None)

    def test_fetch_3(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        receiver.inbox = [
            {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 10,
             'time': timestamp, 'state': 'read'}]
        self.assertEqual(receiver.fetch(), None)

    def test_fetch_4(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        receiver.inbox = [
            {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 10,
             'time':  '2021-01-01 00:00:00', 'state': 'unread'},
            {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 10,
             'time': timestamp, 'state': 'unread'}]
        self.assertEqual(receiver.fetch(), {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 10,
             'time':  '2021-01-01 00:00:00', 'state': 'read'})

    def test_fetch_5(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        receiver.inbox = [
            {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 10,
             'time': '2021-01-01 00:00:00', 'state': 'read'},
            {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 10,
             'time': timestamp, 'state': 'unread'}]
        self.assertEqual(receiver.fetch(), {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 10,
             'time': timestamp, 'state': 'read'})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
