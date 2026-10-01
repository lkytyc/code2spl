class CurrencyConverter:
    def __init__(self):
        self.rates = {
            'USD': 1.0,
            'EUR': 0.85,
            'GBP': 0.72,
            'JPY': 110.15,
            'CAD': 1.23,
            'AUD': 1.34,
            'CNY': 6.40
        }

    def add_currency_rate(self, currency, rate):
        if currency in self.rates:
            return False
        self.rates[currency] = rate

    def convert(self, amount, from_currency, to_currency):
        if from_currency == to_currency:
            return amount
        if from_currency not in self.rates or to_currency not in self.rates:
            return False
        from_rate = self.rates[from_currency]
        to_rate = self.rates[to_currency]
        converted_amount = (amount / from_rate) * to_rate
        return converted_amount

    def get_supported_currencies(self):
        return list(self.rates.keys())

    def update_currency_rate(self, currency, new_rate):
        if currency not in self.rates:
            return False
        self.rates[currency] = new_rate

import unittest

class CurrencyConverterTestGetSupportedCurrencies(unittest.TestCase):
    def test_get_supported_currencies_1(self):
        cc = CurrencyConverter()
        res = cc.get_supported_currencies()
        self.assertEqual(res, ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CNY'])

    def test_get_supported_currencies_2(self):
        cc = CurrencyConverter()
        res = cc.get_supported_currencies()
        self.assertEqual(res, ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CNY'])

    def test_get_supported_currencies_3(self):
        cc = CurrencyConverter()
        res = cc.get_supported_currencies()
        self.assertEqual(res, ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CNY'])

    def test_get_supported_currencies_4(self):
        cc = CurrencyConverter()
        res = cc.get_supported_currencies()
        self.assertEqual(res, ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CNY'])

    def test_get_supported_currencies_5(self):
        cc = CurrencyConverter()
        res = cc.get_supported_currencies()
        self.assertEqual(res, ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CNY'])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
