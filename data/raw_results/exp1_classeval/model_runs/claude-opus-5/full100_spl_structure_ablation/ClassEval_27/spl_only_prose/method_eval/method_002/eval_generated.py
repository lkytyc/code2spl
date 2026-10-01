class CurrencyConverter:
    def __init__(self):
        self.rates = {
            "USD": 1.0,
            "EUR": 0.85,
            "GBP": 0.72,
            "JPY": 110.15,
            "CAD": 1.23,
            "AUD": 1.34,
            "CNY": 6.40,
        }

    def add_currency_rate(self, currency: str, rate: float) -> bool:
        duplicate_check = currency in self.rates
        if duplicate_check:
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

    def get_supported_currencies(self) -> list:
        rates_dict = self.rates
        keys_view = rates_dict.keys()
        currencies = list(keys_view)
        return currencies

    def update_currency_rate(self, currency: str, new_rate) -> bool:
        if currency not in self.rates:
            return False
        self.rates[currency] = new_rate

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
