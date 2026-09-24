class CurrencyConverter:
    def __init__(self):
        self.rates = {
            "USD": 1.0,
            "EUR": 0.89,
            "GBP": 0.76,
            "JPY": 156.0,
            "AUD": 1.5,
            "CAD": 1.36,
            "CHF": 0.97,
            "CNY": 7.15,
            "INR": 83.0,
        }

    def convert(self, amount, source, target):
        if source == target:
            return amount
        if source not in self.rates or target not in self.rates:
            return False
        return (amount / self.rates[source]) * self.rates[target]

    def list_currencies(self):
        return list(self.rates.keys())

    def get_currencies(self):
        return list(self.rates.keys())

    def add_currency(self, currency, rate):
        if currency in self.rates:
            return False
        self.rates[currency] = rate
        return True

    def update_currency(self, currency, rate):
        if currency not in self.rates:
            return False
        self.rates[currency] = rate
        return True

import unittest

class CurrencyConverterTestConvert(unittest.TestCase):
    def test_convert_1(self):
        cc = CurrencyConverter()
        res = cc.convert(64, 'CNY', 'USD')
        self.assertEqual(res, 10.0)

    def test_convert_2(self):
        cc = CurrencyConverter()
        res = cc.convert(64, 'USD', 'USD')
        self.assertEqual(res, 64)

    def test_convert_3(self):
        cc = CurrencyConverter()
        res = cc.convert(64, 'CNY', 'GBP')
        self.assertAlmostEqual(res, 7.1999999999999)

    def test_convert_4(self):
        cc = CurrencyConverter()
        res = cc.convert(64, 'USD', 'GBP')
        self.assertAlmostEqual(res, 46.08)

    def test_convert_5(self):
        cc = CurrencyConverter()
        res = cc.convert(64, 'USD', 'CAD')
        self.assertAlmostEqual(res, 78.72)

    def test_convert_6(self):
        cc = CurrencyConverter()
        res = cc.convert(64, '???', 'USD')
        self.assertFalse(res)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
