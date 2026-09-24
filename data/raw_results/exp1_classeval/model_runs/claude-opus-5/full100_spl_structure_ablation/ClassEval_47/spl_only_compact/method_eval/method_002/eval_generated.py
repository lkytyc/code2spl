class IPAddress:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def get_binary(self):
        is_valid_result = self.is_valid()
        if is_valid_result:
            binary_octets = []
            octets_iterable = self.get_octets()
            for octet in octets_iterable:
                binary_octets.append(format(int(octet), '08b'))
            dotted_binary_string = '.'.join(binary_octets)
            return dotted_binary_string
        return ''

    def get_octets(self):
        is_valid_result = self.is_valid()
        if is_valid_result:
            octets_list = self.ip_address.split('.')
            return octets_list
        return []

    def is_valid(self):
        octets = self.ip_address.split('.')
        if len(octets) != 4:
            return False
        for octet in octets:
            if not octet.isdigit():
                return False
            if int(octet) < 0 or int(octet) > 255:
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
