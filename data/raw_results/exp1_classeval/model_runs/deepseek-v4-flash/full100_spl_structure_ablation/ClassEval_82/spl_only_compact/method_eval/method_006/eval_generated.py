class StockPortfolioTracker:
    def __init__(self, cash_balance: object):
        self.portfolio = []
        self.cash_balance = cash_balance

    def add_stock(self, stock: dict) -> None:
        for pf in self.portfolio:
            if pf['name'] == stock['name']:
                pf['quantity'] += stock['quantity']
                return
        self.portfolio.append(stock)

    def buy_stock(self, stock: dict) -> bool:
        if stock['price'] * stock['quantity'] > self.cash_balance:
            return False
        self.add_stock(stock)
        self.cash_balance -= stock['price'] * stock['quantity']
        return True

    def calculate_portfolio_value(self) -> float:
        total_value = self.cash_balance
        for stock in self.portfolio:
            total_value += stock['price'] * stock['quantity']
        return total_value

    def get_portfolio_summary(self) -> tuple:
        summary = []
        for stock in self.portfolio:
            value = self.get_stock_value(stock)
            summary.append({"name": stock["name"], "value": value})
        portfolio_value = self.calculate_portfolio_value()
        return (portfolio_value, summary)

    def get_stock_value(self, stock: dict) -> float:
        stock_price = stock['price']
        stock_quantity = stock['quantity']
        return stock_price * stock_quantity

    def remove_stock(self, stock: dict) -> bool:
        for pf in self.portfolio:
            if pf['name'] == stock['name'] and pf['quantity'] >= stock['quantity']:
                pf['quantity'] -= stock['quantity']
                if pf['quantity'] == 0:
                    self.portfolio.remove(pf)
                return True
        return False

    def sell_stock(self, stock: dict) -> bool:
        removal_result = self.remove_stock(stock)
        if removal_result == False:
            return False
        self.cash_balance += stock['price'] * stock['quantity']
        return True

import unittest

class StockPortfolioTrackerTestGetStockValue(unittest.TestCase):
    def test_get_stock_value(self):
        tracker = StockPortfolioTracker(10000.0)
        self.assertEqual(tracker.get_stock_value({"name": "AAPL", "price": 150.0, "quantity": 10}), 1500.0)

    def test_get_stock_value_2(self):
        tracker = StockPortfolioTracker(10000.0)
        self.assertEqual(tracker.get_stock_value({"name": "AAPL", "price": 150.0, "quantity": 0}), 0.0)

    def test_get_stock_value_3(self):
        tracker = StockPortfolioTracker(10000.0)
        self.assertEqual(tracker.get_stock_value({"name": "AAPL", "price": 0.0, "quantity": 10}), 0.0)

    def test_get_stock_value_4(self):
        tracker = StockPortfolioTracker(10000.0)
        self.assertEqual(tracker.get_stock_value({"name": "AAPL", "price": 0.0, "quantity": 0}), 0.0)

    def test_get_stock_value_5(self):
        tracker = StockPortfolioTracker(10000.0)
        self.assertEqual(tracker.get_stock_value({"name": "MSFL", "price": 150.0, "quantity": 2}), 300.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
