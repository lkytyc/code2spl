class CurrencyConverter:
    def __init__(self):
        self.rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "GBP": 0.75,
            "JPY": 110.0,
            "CAD": 1.25,
            "AUD": 1.35,
            "CNY": 6.45
        }

    def convert(self, amount, source_currency, target_currency):
        if source_currency == target_currency:
            return amount
        if source_currency not in self.rates or target_currency not in self.rates:
            return False
        amount_in_usd = amount / self.rates[source_currency]
        converted_amount = amount_in_usd * self.rates[target_currency]
        return converted_amount

    def get_supported_currencies(self):
        return list(self.rates.keys())

    def add_currency_rate(self, currency_code, rate):
        if currency_code in self.rates:
            return False
        self.rates[currency_code] = rate
        return True

    def update_currency_rate(self, currency_code, rate):
        if currency_code not in self.rates:
            return False
        self.rates[currency_code] = rate
        return True

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
