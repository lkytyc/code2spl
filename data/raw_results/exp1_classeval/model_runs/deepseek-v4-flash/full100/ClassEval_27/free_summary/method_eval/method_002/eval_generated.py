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

class CurrencyConverterTestAddCurrencyRate(unittest.TestCase):
    def test_add_currency_rate_1(self):
        cc = CurrencyConverter()
        cc.add_currency_rate('KRW', 1308.84)
        self.assertEqual(cc.rates['KRW'], 1308.84)

    def test_add_currency_rate_2(self):
        cc = CurrencyConverter()
        cc.add_currency_rate('aaa', 1.0)
        self.assertEqual(cc.rates['aaa'], 1.0)

    def test_add_currency_rate_3(self):
        cc = CurrencyConverter()
        cc.add_currency_rate('bbb', 2.0)
        self.assertEqual(cc.rates['bbb'], 2.0)

    def test_add_currency_rate_4(self):
        cc = CurrencyConverter()
        cc.add_currency_rate('ccc', 3.0)
        self.assertEqual(cc.rates['ccc'], 3.0)

    def test_add_currency_rate_5(self):
        cc = CurrencyConverter()
        cc.add_currency_rate('ddd', 4.0)
        self.assertEqual(cc.rates['ddd'], 4.0)

    def test_add_currency_rate_6(self):
        cc = CurrencyConverter()
        res = cc.add_currency_rate('USD', 1.0)
        self.assertFalse(res)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
