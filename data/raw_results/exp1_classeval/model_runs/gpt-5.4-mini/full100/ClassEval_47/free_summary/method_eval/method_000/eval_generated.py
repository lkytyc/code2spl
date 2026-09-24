class IPAddress:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def is_valid(self):
        parts = self.ip_address.split(".")
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit():
                return False
            value = int(part)
            if value < 0 or value > 255:
                return False
        return True

    def get_octets(self):
        if not self.is_valid():
            return []
        return self.ip_address.split(".")

    def get_binary(self):
        if not self.is_valid():
            return ""
        octets = self.get_octets()
        binary_octets = [format(int(octet), "08b") for octet in octets]
        return ".".join(binary_octets)

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
