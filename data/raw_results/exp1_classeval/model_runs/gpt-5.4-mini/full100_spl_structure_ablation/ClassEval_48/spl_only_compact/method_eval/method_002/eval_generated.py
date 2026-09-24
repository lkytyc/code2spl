import socket


class IpUtil:
    @staticmethod
    def get_hostname(ip_address: str):
        try:
            return socket.gethostbyaddr(ip_address)[0]
        except socket.herror:
            return None

    @staticmethod
    def is_valid_ipv4(ip_address: str) -> bool:
        try:
            socket.inet_pton(socket.AF_INET, ip_address)
            return True
        except socket.error:
            return False

    @staticmethod
    def is_valid_ipv6(ip_address: str) -> bool:
        try:
            socket.inet_pton(socket.AF_INET6, ip_address)
            return True
        except socket.error:
            return False

import unittest

class IpUtilTestGetHostname(unittest.TestCase):
    def test_get_hostname_1(self):
        result = IpUtil.get_hostname('110.242.68.3')
        self.assertEqual(result, None)

    def test_get_hostname_2(self):
        result = IpUtil.get_hostname('10.0.0.1')
        self.assertEqual(result, None)

    def test_get_hostname_3(self):
        result = IpUtil.get_hostname('0.0.0.0')
        self.assertEqual(result, 'LAPTOP-2CS86KUM')

    def test_get_hostname_4(self):
        result = IpUtil.get_hostname('0.0.0.1')
        self.assertEqual(result, None)

    def test_get_hostname_5(self):
        result = IpUtil.get_hostname('0.0.0.2')
        self.assertEqual(result, None)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
