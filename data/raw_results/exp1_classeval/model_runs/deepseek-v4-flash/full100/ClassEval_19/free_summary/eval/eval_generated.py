class ChandrasekharSieve:
    def __init__(self, n):
        self.n = n
        self.primes = []
        if n >= 2:
            sieve = [True] * (n + 1)
            sieve[0] = sieve[1] = False
            for i in range(2, int(n ** 0.5) + 1):
                if sieve[i]:
                    for j in range(i * i, n + 1, i):
                        sieve[j] = False
            self.primes = [i for i in range(2, n + 1) if sieve[i]]

    def get_primes(self):
        return self.primes

import unittest


class ChandrasekharSieveTestGeneratePrimes(unittest.TestCase):
    def test_generate_primes_1(self):
        cs = ChandrasekharSieve(20)
        res = cs.generate_primes()
        self.assertEqual(res, [2, 3, 5, 7, 11, 13, 17, 19])

    def test_generate_primes_2(self):
        cs = ChandrasekharSieve(18)
        res = cs.generate_primes()
        self.assertEqual(res, [2, 3, 5, 7, 11, 13, 17])

    def test_generate_primes_3(self):
        cs = ChandrasekharSieve(15)
        res = cs.generate_primes()
        self.assertEqual(res, [2, 3, 5, 7, 11, 13])

    def test_generate_primes_4(self):
        cs = ChandrasekharSieve(10)
        res = cs.generate_primes()
        self.assertEqual(res, [2, 3, 5, 7])

    def test_generate_primes_5(self):
        cs = ChandrasekharSieve(1)
        res = cs.generate_primes()
        self.assertEqual(res, [])


class ChandrasekharSieveTestGetPrimes(unittest.TestCase):
    def test_get_primes_1(self):
        cs = ChandrasekharSieve(20)
        cs.generate_primes()
        res = cs.get_primes()
        self.assertEqual(res, [2, 3, 5, 7, 11, 13, 17, 19])

    def test_get_primes_2(self):
        cs = ChandrasekharSieve(18)
        cs.generate_primes()
        res = cs.get_primes()
        self.assertEqual(res, [2, 3, 5, 7, 11, 13, 17])

    def test_get_primes_3(self):
        cs = ChandrasekharSieve(15)
        cs.generate_primes()
        res = cs.get_primes()
        self.assertEqual(res, [2, 3, 5, 7, 11, 13])

    def test_get_primes_4(self):
        cs = ChandrasekharSieve(10)
        cs.generate_primes()
        res = cs.get_primes()
        self.assertEqual(res, [2, 3, 5, 7])

    def test_get_primes_5(self):
        cs = ChandrasekharSieve(1)
        res = cs.get_primes()
        self.assertEqual(res, [])


class ChandrasekharSieveTest(unittest.TestCase):
    def test_chandrasekharsieve(self):
        cs = ChandrasekharSieve(20)
        res = cs.generate_primes()
        self.assertEqual(res, [2, 3, 5, 7, 11, 13, 17, 19])
        res = cs.get_primes()
        self.assertEqual(res, [2, 3, 5, 7, 11, 13, 17, 19])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
