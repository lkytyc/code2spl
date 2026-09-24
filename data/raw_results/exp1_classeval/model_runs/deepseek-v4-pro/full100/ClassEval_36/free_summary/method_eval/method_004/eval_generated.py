class EmailClient:
    def __init__(self, addr, capacity):
        self.addr = addr
        self.capacity = capacity
        self.inbox = []

    def send_to(self, receiver, content, size):
        if receiver.is_full_with_one_more_email(size):
            self.clear_inbox(size)
            return False
        email = {
            "sender": self.addr,
            "receiver": receiver.addr,
            "content": content,
            "size": size,
            "timestamp": self._current_timestamp(),
            "state": "unread"
        }
        receiver.inbox.append(email)
        return True

    def fetch(self):
        for email in self.inbox:
            if email["state"] == "unread":
                email["state"] = "read"
                return email
        return None

    def is_full_with_one_more_email(self, size):
        occupied = sum(e["size"] for e in self.inbox)
        return occupied + size > self.capacity

    def clear_inbox(self, size):
        occupied = sum(e["size"] for e in self.inbox)
        while self.inbox and occupied + size > self.capacity:
            removed = self.inbox.pop(0)
            occupied -= removed["size"]

    def _current_timestamp(self):
        import time
        return time.time()

import unittest

class EmailClientTestClearInbox(unittest.TestCase):
    def test_clear_inbox(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        receiver.inbox = [{'size': 10},{'size': 20},{'size': 15}]
        receiver.clear_inbox(30)
        self.assertEqual(receiver.inbox, [{'size': 15}])

    def test_clear_inbox_2(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('', 50)
        receiver.inbox = [{'size': 10},{'size': 20},{'size': 15}]
        self.assertEqual(receiver.clear_inbox(30),None)
        self.assertEqual(receiver.inbox, [{'size': 10},{'size': 20},{'size': 15}])

    def test_clear_inbox_3(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        receiver.inbox = [{'size': 10}, {'size': 20}, {'size': 15}]
        self.assertEqual(receiver.clear_inbox(50), None)

    def test_clear_inbox_4(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        receiver.inbox = [{'size': 10}, {'size': 20}, {'size': 15}]
        receiver.clear_inbox(45)
        self.assertEqual(receiver.inbox, [])
    def test_clear_inbox_5(self):
        sender = EmailClient('sender@example.com', 100)
        receiver = EmailClient('receiver@example.com', 50)
        receiver.inbox = [{'size': 10}, {'size': 20}, {'size': 15}]
        receiver.clear_inbox(10)
        self.assertEqual(receiver.inbox, [{'size': 20}, {'size': 15}])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
