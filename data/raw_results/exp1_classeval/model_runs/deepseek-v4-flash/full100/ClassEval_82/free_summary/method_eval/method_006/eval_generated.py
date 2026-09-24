class StockPortfolioTracker:
    def __init__(self, starting_cash=0.0):
        self.cash = starting_cash
        self.portfolio = []

    def _find_stock(self, name):
        for stock in self.portfolio:
            if stock["name"] == name:
                return stock
        return None

    def add_stock(self, name, quantity, price):
        if quantity <= 0 or price < 0:
            return False
        stock = self._find_stock(name)
        if stock is None:
            self.portfolio.append({"name": name, "quantity": quantity, "price": price})
        else:
            stock["quantity"] += quantity
            stock["price"] = price
        return True

    def remove_stock(self, name, quantity):
        if quantity <= 0:
            return False
        stock = self._find_stock(name)
        if stock is None or stock["quantity"] < quantity:
            return False
        stock["quantity"] -= quantity
        if stock["quantity"] == 0:
            self.portfolio.remove(stock)
        return True

    def buy_stock(self, name, quantity, price):
        if quantity <= 0 or price < 0:
            return False
        cost = quantity * price
        if self.cash < cost:
            return False
        self.cash -= cost
        stock = self._find_stock(name)
        if stock is None:
            self.portfolio.append({"name": name, "quantity": quantity, "price": price})
        else:
            stock["quantity"] += quantity
            stock["price"] = price
        return True

    def sell_stock(self, name, quantity, price):
        if quantity <= 0 or price < 0:
            return False
        stock = self._find_stock(name)
        if stock is None or stock["quantity"] < quantity:
            return False
        stock["quantity"] -= quantity
        self.cash += quantity * price
        if stock["quantity"] == 0:
            self.portfolio.remove(stock)
        else:
            stock["price"] = price
        return True

    def total_value(self):
        return self.cash + sum(stock["quantity"] * stock["price"] for stock in self.portfolio)

    def portfolio_value(self):
        return self.total_value()

    def summary(self):
        holdings = [
            {
                "name": stock["name"],
                "quantity": stock["quantity"],
                "price": stock["price"],
                "market_value": stock["quantity"] * stock["price"],
            }
            for stock in self.portfolio
        ]
        return self.total_value(), holdings

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
