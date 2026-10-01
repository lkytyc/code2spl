import socket


class IpUtil:
    def get_hostname(self, ip_address: str):
        try:
            host_lookup_result = socket.gethostbyaddr(ip_address)
            hostname = host_lookup_result[0]
            return hostname
        except socket.herror:
            return None

    def is_valid_ipv4(self, ip_address: str) -> bool:
        try:
            socket.inet_pton(socket.AF_INET, ip_address)
            return True
        except socket.error:
            return False

    def is_valid_ipv6(self, ip_address: str) -> bool:
        try:
            socket.inet_pton(socket.AF_INET6, ip_address)
            return True
        except socket.error:
            return False

import unittest

class IpUtilTestIsValidIpv4(unittest.TestCase):
    def test_is_valid_ipv4_1(self):
        result = IpUtil.is_valid_ipv4('192.168.0.123')
        self.assertEqual(result, True)

    def test_is_valid_ipv4_2(self):
        result = IpUtil.is_valid_ipv4('10.10.10.10')
        self.assertEqual(result, True)

    def test_is_valid_ipv4_3(self):
        result = IpUtil.is_valid_ipv4('0.0.0.0')
        self.assertEqual(result, True)

    def test_is_valid_ipv4_4(self):
        result = IpUtil.is_valid_ipv4('abc.168.0.123')
        self.assertEqual(result, False)

    def test_is_valid_ipv4_5(self):
        result = IpUtil.is_valid_ipv4('256.0.0.0')
        self.assertEqual(result, False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
