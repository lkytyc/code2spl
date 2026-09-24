class IPAddress:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def is_valid(self):
        octets = self.ip_address.split('.')
        if len(octets) != 4:
            return False
        for octet in octets:
            if not octet.isdigit() or int(octet) < 0 or int(octet) > 255:
                return False
        return True

    def get_octets(self):
        if self.is_valid():
            return self.ip_address.split('.')
        return []

    def get_binary(self):
        if not self.is_valid():
            return ''
        binary_octets = []
        for octet in self.get_octets():
            binary_string = format(int(octet), '08b')
            binary_octets.append(binary_string)
        return '.'.join(binary_octets)

import unittest

class IPAddressTestIsValid(unittest.TestCase):
    def test_is_valid_1(self):
        ipaddress = IPAddress("10.10.10.10")
        self.assertEqual(ipaddress.is_valid(), True)

    def test_is_valid_2(self):
        ipaddress = IPAddress("-1.10.10.10")
        self.assertEqual(ipaddress.is_valid(), False)

    def test_is_valid_3(self):
        ipaddress = IPAddress("10.10.10")
        self.assertEqual(ipaddress.is_valid(), False)

    def test_is_valid_4(self):
        ipaddress = IPAddress("a.10.10.10")
        self.assertEqual(ipaddress.is_valid(), False)

    def test_is_valid_5(self):
        ipaddress = IPAddress("300.10.10.10")
        self.assertEqual(ipaddress.is_valid(), False)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
