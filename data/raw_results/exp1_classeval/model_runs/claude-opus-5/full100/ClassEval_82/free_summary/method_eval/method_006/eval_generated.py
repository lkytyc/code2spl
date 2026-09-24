class StockPortfolioTracker:
    def __init__(self, cash_balance: float):
        self.portfolio = []
        self.cash_balance = cash_balance

    def add_stock(self, stock: dict):
        for holding in self.portfolio:
            if holding["name"] == stock["name"]:
                holding["quantity"] += stock["quantity"]
                return
        self.portfolio.append({"name": stock["name"], "quantity": stock["quantity"], "price": stock["price"]})

    def remove_stock(self, stock: dict) -> bool:
        for i, holding in enumerate(self.portfolio):
            if holding["name"] == stock["name"]:
                if holding["quantity"] < stock["quantity"]:
                    return False
                holding["quantity"] -= stock["quantity"]
                if holding["quantity"] == 0:
                    self.portfolio.pop(i)
                return True
        return False

    def buy_stock(self, stock: dict) -> bool:
        total_cost = stock["price"] * stock["quantity"]
        if total_cost > self.cash_balance:
            return False
        self.add_stock(stock)
        self.cash_balance -= total_cost
        return True

    def sell_stock(self, stock: dict) -> bool:
        if not self.remove_stock(stock):
            return False
        self.cash_balance += stock["price"] * stock["quantity"]
        return True

    def get_stock_value(self, stock: dict) -> float:
        return stock["price"] * stock["quantity"]

    def calculate_portfolio_value(self) -> float:
        return sum(self.get_stock_value(holding) for holding in self.portfolio) + self.cash_balance

    def get_portfolio_summary(self) -> tuple:
        summary = [{"name": holding["name"], "value": self.get_stock_value(holding)} for holding in self.portfolio]
        total_value = self.calculate_portfolio_value()
        return total_value, summary

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
