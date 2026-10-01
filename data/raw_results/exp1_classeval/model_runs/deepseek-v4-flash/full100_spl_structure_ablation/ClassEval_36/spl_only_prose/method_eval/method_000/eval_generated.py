class EmailClient:
    def __init__(self, addr: object, capacity: object):
        self.addr = addr
        self.capacity = capacity
        self.inbox = []

    def clear_inbox(self, size: int) -> None:
        if not self.addr:
            return None
        freed_space = 0
        while freed_space < size and self.inbox:
            email = self.inbox[0]
            freed_space += email['size']
            del self.inbox[0]

    def fetch(self) -> object or None:
        for i in range(len(self.inbox)):
            if self.inbox[i]['state'] == 'unread':
                self.inbox[i]['state'] = 'read'
                return self.inbox[i]
        return None

    def get_occupied_size(self) -> int:
        occupied_size = 0
        for email in self.inbox:
            occupied_size += email['size']
        return occupied_size

    def is_full_with_one_more_email(self, size: int) -> bool:
        occupied_size = self.get_occupied_size()
        return occupied_size + size > self.capacity

    def send_to(self, recv: object, content: any, size: int) -> bool:
        not_full = not recv.is_full_with_one_more_email(size)
        if not_full:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            email = {
                'sender': self.addr,
                'receiver': recv.addr,
                'content': content,
                'size': size,
                'timestamp': timestamp,
                'state': 'unread'
            }
            recv.inbox.append(email)
            return True
        else:
            self.clear_inbox(size)
            return False

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
