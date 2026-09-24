class Server:
    def __init__(self):
        self.white_list = []
        self.send_struct = None
        self.receive_struct = None

    def add_white_list(self, addr):
        if addr in self.white_list:
            return False
        self.white_list.append(addr)
        return self.white_list

    def del_white_list(self, addr):
        if addr not in self.white_list:
            return False
        self.white_list.remove(addr)
        return self.white_list

    def recv(self, data):
        if not isinstance(data, dict) or "addr" not in data or "content" not in data:
            return -1
        if data["addr"] not in self.white_list:
            return False
        self.receive_struct = data
        return data["content"]

    def send(self, data):
        if not isinstance(data, dict) or "addr" not in data or "content" not in data:
            return "Invalid input"
        self.send_struct = data
        return None

    def show(self, type):
        if type == "send":
            return self.send_struct
        if type in ("recv", "receive"):
            return self.receive_struct
        return False

import unittest

class ServerTestShow(unittest.TestCase):
    def test_show_1(self):
        server = Server()
        server.add_white_list(66)
        server.send({"addr": 88, "content": "abc"})
        server.recv({"addr": 66, "content": "ABC"})
        self.assertEqual(server.show("send"), {"addr": 88, "content": "abc"})

    def test_show_2(self):
        server = Server()
        server.add_white_list(66)
        server.send({"addr": 88, "content": "abc"})
        server.recv({"addr": 66, "content": "ABC"})
        self.assertEqual(server.show("receive"), {"addr": 66, "content": "ABC"})

    def test_show_3(self):
        server = Server()
        server.add_white_list(66)
        server.send({"addr": 88, "content": "abc"})
        server.recv({"addr": 66, "content": "ABC"})
        self.assertEqual(server.show("abcdefg"), False)

    def test_show_4(self):
        server = Server()
        server.add_white_list(66)
        server.send({"addr": 11, "content": "abc"})
        server.recv({"addr": 66, "content": "ABC"})
        self.assertEqual(server.show("send"), {"addr": 11, "content": "abc"})

    def test_show_5(self):
        server = Server()
        server.add_white_list(66)
        server.send({"addr": 22, "content": "abc"})
        server.recv({"addr": 66, "content": "ABC"})
        self.assertEqual(server.show("send"), {"addr": 22, "content": "abc"})

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
