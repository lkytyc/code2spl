class IPAddress:
    def __init__(self, address):
        self.address = address
        parts = address.split(".")
        self.octets = []
        self._valid = False

        if len(parts) == 4:
            valid = True
            for part in parts:
                if not part.isdecimal() or not 0 <= int(part) <= 255:
                    valid = False
                    break
            if valid:
                self._valid = True
                self.octets = parts

    def get_octets(self):
        return list(self.octets)

    def get_binary(self):
        if not self._valid:
            return ""
        return ".".join(format(int(octet), "08b") for octet in self.octets)

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
