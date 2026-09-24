class IPAddress:
    def __init__(self, address):
        self.address = address

    def is_valid(self):
        parts = self.address.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            try:
                value = int(part)
            except ValueError:
                return False
            if value < 0 or value > 255:
                return False
        return True

    def get_octets(self):
        if not self.is_valid():
            return []
        return self.address.split('.')

    def get_binary(self):
        if not self.is_valid():
            return ''
        return '.'.join(format(int(octet), '08b') for octet in self.address.split('.'))

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
