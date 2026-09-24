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
