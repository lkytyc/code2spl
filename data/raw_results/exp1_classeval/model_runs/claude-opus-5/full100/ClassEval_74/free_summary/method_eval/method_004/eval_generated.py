class Server:
    def __init__(self):
        self.white_list = []
        self.send_struct = {}
        self.receive_struct = {}

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

    def recv(self, info):
        if not isinstance(info, dict):
            return -1
        if 'addr' not in info or 'content' not in info:
            return -1
        if info['addr'] not in self.white_list:
            return False
        self.receive_struct = {'addr': info['addr'], 'content': info['content']}
        return info['content']

    def send(self, info):
        if not isinstance(info, dict):
            return "info structure is not correct"
        if 'addr' not in info or 'content' not in info:
            return "info structure is not correct"
        self.send_struct = {'addr': info['addr'], 'content': info['content']}
        return None

    def show(self, key):
        if key == 'send':
            return self.send_struct
        elif key == 'receive':
            return self.receive_struct
        else:
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
