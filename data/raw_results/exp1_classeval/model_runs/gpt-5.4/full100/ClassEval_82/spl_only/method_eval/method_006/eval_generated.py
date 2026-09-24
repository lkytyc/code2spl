class StockPortfolioTracker:
    def __init__(self, cash_balance):
        self.portfolio = []
        self.cash_balance = cash_balance

    def add_stock(self, stock):
        for pf in self.portfolio:
            if pf["name"] == stock["name"]:
                pf["quantity"] += stock["quantity"]
                return
        self.portfolio.append(stock)

    def remove_stock(self, stock):
        for pf in self.portfolio:
            if pf["name"] == stock["name"] and pf["quantity"] >= stock["quantity"]:
                pf["quantity"] -= stock["quantity"]
                if pf["quantity"] == 0:
                    self.portfolio.remove(pf)
                return True
        return False

    def buy_stock(self, stock):
        cost = stock["price"] * stock["quantity"]
        if cost > self.cash_balance:
            return False
        self.add_stock(stock)
        self.cash_balance -= cost
        return True

    def sell_stock(self, stock):
        remove_result = self.remove_stock(stock)
        if not remove_result:
            return False
        self.cash_balance += stock["price"] * stock["quantity"]
        return True

    def calculate_portfolio_value(self):
        total_value = self.cash_balance
        for stock in self.portfolio:
            total_value += stock["price"] * stock["quantity"]
        return total_value

    def get_portfolio_summary(self):
        summary = []
        for stock in self.portfolio:
            summary.append({"name": stock["name"], "value": self.get_stock_value(stock)})
        portfolio_value = self.calculate_portfolio_value()
        return portfolio_value, summary

    def get_stock_value(self, stock):
        price = stock["price"]
        quantity = stock["quantity"]
        return price * quantity

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
