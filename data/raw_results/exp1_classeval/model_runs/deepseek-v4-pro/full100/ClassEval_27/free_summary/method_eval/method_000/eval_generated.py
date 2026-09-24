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
