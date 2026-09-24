class IPAddress:
    def __init__(self, ip_address: str):
        self.ip_address = ip_address

    def get_binary(self) -> str:
        if not self.is_valid():
            return ''
        binary_octets = []
        for octet in self.get_octets():
            binary_string = format(int(octet), '08b')
            binary_octets.append(binary_string)
        joined_binary = '.'.join(binary_octets)
        return joined_binary

    def get_octets(self) -> list:
        validity_result = self.is_valid()
        if validity_result:
            return self.ip_address.split('.')
        return []

    def is_valid(self) -> bool:
        octets = self.ip_address.split('.')
        if len(octets) != 4:
            return False
        for octet in octets:
            if not octet.isdigit() or int(octet) < 0 or int(octet) > 255:
                return False
        return True

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
