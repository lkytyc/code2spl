class ChandrasekharSieve:
    def __init__(self, n):
        self.n = n
        self.primes = []
        self.generate_primes()

    def generate_primes(self):
        if self.n < 2:
            self.primes = []
            return
        is_prime = [True] * (self.n + 1)
        is_prime[0] = is_prime[1] = False
        p = 2
        while p * p <= self.n:
            if is_prime[p]:
                for multiple in range(p * p, self.n + 1, p):
                    is_prime[multiple] = False
            p += 1
        self.primes = [i for i, prime in enumerate(is_prime) if prime]

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

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
