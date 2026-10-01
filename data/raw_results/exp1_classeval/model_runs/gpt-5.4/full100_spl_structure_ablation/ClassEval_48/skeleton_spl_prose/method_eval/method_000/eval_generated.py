class IpUtil:
    """
    This is a class as tool for ip that can be used to obtain the local IP address, validate its validity, and also provides the functionality to retrieve the corresponding hostname.
    """

    @staticmethod
    def is_valid_ipv4(ip_address):
        """
        Check if the given IP address is a valid IPv4 address.
        :param ip_address: string, the IP address to check
        :return: bool, True if the IP address is valid, False otherwise
        """
        try:
            socket.inet_pton(socket.AF_INET, ip_address)
            return True
        except socket.error:
            return False

    @staticmethod
    def is_valid_ipv6(ip_address):
        """
        Check if the given IP address is a valid IPv6 address.
        :param ip_address: string, the IP address to check
        :return: bool, True if the IP address is valid, False otherwise
        """
        try:
            socket.inet_pton(socket.AF_INET6, ip_address)
            return True
        except socket.error:
            return False

    @staticmethod
    def get_hostname(ip_address):
        """
        Get the hostname associated with the given IP address.
        :param ip_address: string, the IP address to get the hostname for
        :return: string, the hostname associated with the IP address
        """
        try:
            host_lookup_result = socket.gethostbyaddr(ip_address)
            hostname = host_lookup_result[0]
            return hostname
        except socket.herror:
            return None

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
