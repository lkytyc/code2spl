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
