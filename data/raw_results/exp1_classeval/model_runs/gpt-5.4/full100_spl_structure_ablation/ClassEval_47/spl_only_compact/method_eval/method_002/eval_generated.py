class IPAddress:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def get_binary(self):
        is_valid = self.is_valid()
        if is_valid:
            binary_octets = []
            for octet in self.get_octets():
                binary_octet = format(int(octet), "08b")
                binary_octets.append(binary_octet)
            result = ".".join(binary_octets)
            return result
        return ""

    def get_octets(self):
        is_valid = self.is_valid()
        if is_valid:
            return self.ip_address.split(".")
        return []

    def is_valid(self):
        octets = self.ip_address.split(".")
        octet_count_invalid = len(octets) != 4
        if octet_count_invalid:
            return False

        for octet in octets:
            octet_invalid = (
                not octet.isdigit()
                or int(octet) < 0
                or int(octet) > 255
            )
            if octet_invalid:
                return False

        return True

import unittest

class IPAddressTestGetBinary(unittest.TestCase):
    def test_get_binary_1(self):
        ipaddress = IPAddress("10.10.10.10")
        self.assertEqual(ipaddress.get_binary(), "00001010.00001010.00001010.00001010")

    def test_get_binary_2(self):
        ipaddress = IPAddress("a.10.10.10")
        self.assertEqual(ipaddress.get_binary(), '')

    def test_get_binary_3(self):
        ipaddress = IPAddress("-1.10.10.10")
        self.assertEqual(ipaddress.get_binary(), '')

    def test_get_binary_4(self):
        ipaddress = IPAddress("300.10.10.10")
        self.assertEqual(ipaddress.get_binary(), '')

    def test_get_binary_5(self):
        ipaddress = IPAddress(".10.10.10")
        self.assertEqual(ipaddress.get_binary(), '')

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
