class IPAddress:
    def __init__(self, ip_address):
        self.ip_address = ip_address

    def is_valid(self):
        parts = self.ip_address.split(".")
        if len(parts) != 4:
            return False

        for part in parts:
            if not part:
                return False
            for ch in part:
                if ch not in "0123456789":
                    return False
            if int(part) > 255:
                return False

        return True

    def get_octets(self):
        if not self.is_valid():
            return []
        return self.ip_address.split(".")

    def get_binary(self):
        if not self.is_valid():
            return ""

        binary_parts = []
        for octet in self.get_octets():
            binary_parts.append(format(int(octet), "08b"))

        return ".".join(binary_parts)

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
