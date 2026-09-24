class IPAddress:
    def __init__(self, ip):
        self.ip = ip

    def is_valid(self):
        parts = self.ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit():
                return False
            num = int(part)
            if num < 0 or num > 255:
                return False
        return True

    def get_octets(self):
        if not self.is_valid():
            return []
        return self.ip.split('.')

    def get_binary(self):
        if not self.is_valid():
            return ""
        octets = self.get_octets()
        binary_octets = [format(int(octet), '08b') for octet in octets]
        return '.'.join(binary_octets)

import unittest

class IPAddressTestGetOctets(unittest.TestCase):
    def test_get_octets_1(self):
        ipaddress = IPAddress("10.10.10.10")
        self.assertEqual(ipaddress.get_octets(), ["10", "10", "10", "10"])

    def test_get_octets_2(self):
        ipaddress = IPAddress("a.10.10.10")
        self.assertEqual(ipaddress.get_octets(), [])

    def test_get_octets_3(self):
        ipaddress = IPAddress("-1.10.10.10")
        self.assertEqual(ipaddress.get_octets(), [])

    def test_get_octets_4(self):
        ipaddress = IPAddress("300.10.10.10")
        self.assertEqual(ipaddress.get_octets(), [])

    def test_get_octets_5(self):
        ipaddress = IPAddress(".10.10.10")
        self.assertEqual(ipaddress.get_octets(), [])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
