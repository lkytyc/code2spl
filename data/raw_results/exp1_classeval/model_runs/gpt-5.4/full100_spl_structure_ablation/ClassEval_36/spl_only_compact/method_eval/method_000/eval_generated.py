class EmailClient:
    def __init__(self, addr, capacity):
        self.addr = addr
        self.capacity = capacity
        self.inbox = []

    def clear_inbox(self, size):
        if len(self.addr) == 0:
            return

        freed_space = 0
        while freed_space < size and self.inbox:
            email = self.inbox[0]
            freed_space += email["size"]
            self.inbox.pop(0)

    def fetch(self):
        if len(self.inbox) == 0:
            return None

        for i in range(len(self.inbox)):
            if self.inbox[i]["state"] == "unread":
                self.inbox[i]["state"] = "read"
                return self.inbox[i]

        return None

    def get_occupied_size(self):
        occupied_size = 0
        for email in self.inbox:
            occupied_size += email["size"]
        return occupied_size

    def is_full_with_one_more_email(self, size):
        occupied_size = self.get_occupied_size()
        is_over_capacity = occupied_size + size > self.capacity
        return True if is_over_capacity else False

    def send_to(self, recv, content, size):
        capacity_ok = not recv.is_full_with_one_more_email(size)

        if capacity_ok:
            import datetime

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            email = {
                "sender": self.addr,
                "receiver": recv.addr,
                "content": content,
                "size": size,
                "timestamp": timestamp,
                "state": "unread",
            }
            recv.inbox.append(email)
            return True

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
