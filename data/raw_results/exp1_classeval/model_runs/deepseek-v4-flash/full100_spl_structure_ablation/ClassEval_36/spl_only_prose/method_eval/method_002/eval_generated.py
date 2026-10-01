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
