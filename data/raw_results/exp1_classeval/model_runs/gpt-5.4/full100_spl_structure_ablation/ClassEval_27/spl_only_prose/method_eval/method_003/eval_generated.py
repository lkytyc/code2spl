class CurrencyConverter:
    def __init__(self):
        self.rates = {
            'USD': 1.0,
            'EUR': 0.85,
            'GBP': 0.72,
            'JPY': 110.15,
            'CAD': 1.23,
            'AUD': 1.34,
            'CNY': 6.40,
        }

    def add_currency_rate(self, currency, rate):
        currency_exists = currency in self.rates
        if currency_exists:
            return False
        self.rates[currency] = rate

    def convert(self, amount, from_currency, to_currency):
        currency_comparison = from_currency != to_currency
        if not currency_comparison:
            return amount

        rate_availability_check = (
            from_currency not in self.rates or to_currency not in self.rates
        )
        if rate_availability_check:
            return False

        from_rate = self.rates[from_currency]
        to_rate = self.rates[to_currency]
        converted_amount = (amount / from_rate) * to_rate
        return converted_amount

    def get_supported_currencies(self):
        rate_keys_view = self.rates.keys()
        supported_currencies = list(rate_keys_view)
        return supported_currencies

    def update_currency_rate(self, currency, new_rate):
        currency_exists = currency in self.rates
        if not currency_exists:
            return False
        self.rates[currency] = new_rate

import unittest

class CurrencyConverterTestUpdateCurrencyRate(unittest.TestCase):
    def test_update_currency_rate_1(self):
        cc = CurrencyConverter()
        cc.update_currency_rate('CNY', 7.18)
        self.assertEqual(cc.rates['CNY'], 7.18)

    def test_update_currency_rate_2(self):
        cc = CurrencyConverter()
        cc.update_currency_rate('CNY', 1.0)
        self.assertEqual(cc.rates['CNY'], 1.0)

    def test_update_currency_rate_3(self):
        cc = CurrencyConverter()
        cc.update_currency_rate('CNY', 2.0)
        self.assertEqual(cc.rates['CNY'], 2.0)

    def test_update_currency_rate_4(self):
        cc = CurrencyConverter()
        cc.update_currency_rate('CNY', 3.0)
        self.assertEqual(cc.rates['CNY'], 3.0)

    def test_update_currency_rate_5(self):
        cc = CurrencyConverter()
        cc.update_currency_rate('CNY', 4.0)
        self.assertEqual(cc.rates['CNY'], 4.0)

    def test_update_currency_rate_6(self):
        cc = CurrencyConverter()
        res = cc.update_currency_rate('???', 7.18)
        self.assertFalse(res)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
