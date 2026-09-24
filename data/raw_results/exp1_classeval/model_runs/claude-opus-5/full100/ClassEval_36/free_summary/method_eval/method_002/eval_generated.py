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

class EmailClientTestIsFullWithOneMoreEmail(unittest.TestCase):
    def test_is_full_with_one_more_email(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        self.assertFalse(receiver.is_full_with_one_more_email(10))

    def test_is_full_with_one_more_email_2(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 0)
        self.assertTrue(receiver.is_full_with_one_more_email(10))

    def test_is_full_with_one_more_email_3(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 10)
        self.assertFalse(receiver.is_full_with_one_more_email(10))

    def test_is_full_with_one_more_email_4(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 10)
        self.assertTrue(receiver.is_full_with_one_more_email(20))

    def test_is_full_with_one_more_email_5(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 20)
        self.assertFalse(receiver.is_full_with_one_more_email(20))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
