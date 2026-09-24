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
        if not isinstance(info, dict) or 'addr' not in info or 'content' not in info:
            return -1
        addr = info['addr']
        content = info['content']
        if addr not in self.white_list:
            return False
        self.receive_struct = {'addr': addr, 'content': content}
        return self.receive_struct['content']

    def send(self, info):
        if not isinstance(info, dict) or 'addr' not in info or 'content' not in info:
            return 'info structure is not correct'
        self.send_struct = {'addr': info['addr'], 'content': info['content']}

    def show(self, type):
        if type == "send":
            return self.send_struct
        elif type == "receive":
            return self.receive_struct
        else:
            return False

import unittest

class ServerTestAddWhiteList(unittest.TestCase):
    def test_add_white_list_1(self):
        server = Server()
        server.add_white_list(88)
        self.assertEqual(server.white_list, [88])

    def test_add_white_list_2(self):
        server = Server()
        server.add_white_list(88)
        self.assertEqual(server.add_white_list(88), False)

    def test_add_white_list_3(self):
        server = Server()
        server.add_white_list(88)
        server.add_white_list(11)
        self.assertEqual(server.add_white_list(11), False)

    def test_add_white_list_4(self):
        server = Server()
        server.add_white_list(11)
        self.assertEqual(server.white_list, [11])

    def test_add_white_list_5(self):
        server = Server()
        server.add_white_list(88)
        server.add_white_list(11)
        server.add_white_list(22)
        self.assertEqual(server.add_white_list(22), False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
