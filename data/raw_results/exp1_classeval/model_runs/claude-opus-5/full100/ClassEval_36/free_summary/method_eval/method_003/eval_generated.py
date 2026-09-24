import datetime


class EmailClient:
    def __init__(self, addr, capacity):
        self.addr = addr
        self.capacity = capacity
        self.inbox = []

    def send_to(self, recipient, content, size):
        if recipient.is_full_with_one_more_email(size):
            self.clear_inbox(size)
            return False
        email = {
            "sender": self.addr,
            "receiver": recipient.addr,
            "content": content,
            "size": size,
            "time": datetime.datetime.now(),
            "state": "unread",
        }
        recipient.inbox.append(email)
        return True

    def fetch(self):
        if not self.inbox:
            return None
        for email in self.inbox:
            if email["state"] == "unread":
                email["state"] = "read"
                return email
        return None

    def is_full_with_one_more_email(self, size):
        return self.get_occupied_size() + size > self.capacity

    def get_occupied_size(self):
        return sum(email["size"] for email in self.inbox)

    def clear_inbox(self, size):
        if self.addr == "":
            return
        freed = 0
        while freed < size and self.inbox:
            email = self.inbox.pop(0)
            freed += email["size"]

import unittest

class EmailClientTestGetOccupiedSize(unittest.TestCase):
    def test_get_occupied_size(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        sender.inbox = [{'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 10, 'time': datetime.now, 'state': 'unread'}]
        self.assertEqual(sender.get_occupied_size(), 10)

    def test_get_occupied_size_2(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        sender.inbox =[]
        self.assertEqual(sender.get_occupied_size(), 0)

    def test_get_occupied_size_3(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        sender.inbox = [
            {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 20,
             'time': datetime.now, 'state': 'unread'}]
        self.assertEqual(sender.get_occupied_size(), 20)

    def test_get_occupied_size_4(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        sender.inbox = [
            {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 20,
             'time': datetime.now, 'state': 'unread'},
            {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 30,
             'time': datetime.now, 'state': 'unread'}]
        self.assertEqual(sender.get_occupied_size(), 50)

    def test_get_occupied_size_5(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        sender.inbox = [
            {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 20,
             'time': datetime.now, 'state': 'unread'},
            {'sender': 'sender@example.com', 'receiver': 'receiver@example.com', 'content': 'Hello', 'size': 60,
             'time': datetime.now, 'state': 'unread'}]
        self.assertEqual(sender.get_occupied_size(), 80)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
