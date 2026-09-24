import socket

class IpUtil:
    @staticmethod
    def is_valid_ipv4(ip):
        try:
            socket.inet_pton(socket.AF_INET, ip)
            return True
        except (socket.error, ValueError):
            return False

    @staticmethod
    def is_valid_ipv6(ip):
        try:
            socket.inet_pton(socket.AF_INET6, ip)
            return True
        except (socket.error, ValueError):
            return False

    @staticmethod
    def get_hostname(ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except (socket.herror, socket.gaierror, OSError):
            return None

import unittest

class IpUtilTestIsValidIpv6(unittest.TestCase):
    def test_is_valid_ipv6_1(self):
        result = IpUtil.is_valid_ipv6('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertEqual(result, True)

    def test_is_valid_ipv6_2(self):
        result = IpUtil.is_valid_ipv6('2001:0db8:85a3:::8a2e:0370:7334')
        self.assertEqual(result, False)

    def test_is_valid_ipv6_3(self):
        result = IpUtil.is_valid_ipv6('2001:0db8:85a3:2001:llll:8a2e:0370:7334')
        self.assertEqual(result, False)

    def test_is_valid_ipv6_4(self):
        result = IpUtil.is_valid_ipv6('2001:0db8:85a3:llll:llll:8a2e:0370:7334')
        self.assertEqual(result, False)

    def test_is_valid_ipv6_5(self):
        result = IpUtil.is_valid_ipv6('2001:0db8:85a3::llll:8a2e:0370:7334')
        self.assertEqual(result, False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
