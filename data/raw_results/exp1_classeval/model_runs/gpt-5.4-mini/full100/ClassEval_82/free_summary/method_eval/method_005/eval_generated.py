class StockPortfolioTracker:
    def __init__(self, cash_balance):
        self.cash_balance = cash_balance
        self.portfolio = []

    def add_stock(self, stock):
        name = stock.get("name")
        price = stock.get("price", 0)
        quantity = stock.get("quantity", 0)

        for holding in self.portfolio:
            if holding.get("name") == name:
                holding["quantity"] = holding.get("quantity", 0) + quantity
                if "price" in stock:
                    holding["price"] = price
                return

        self.portfolio.append({"name": name, "price": price, "quantity": quantity})

    def remove_stock(self, stock):
        name = stock.get("name")
        quantity = stock.get("quantity", 0)

        for i, holding in enumerate(self.portfolio):
            if holding.get("name") == name:
                if holding.get("quantity", 0) < quantity:
                    return False
                holding["quantity"] -= quantity
                if holding["quantity"] == 0:
                    self.portfolio.pop(i)
                return True
        return False

    def buy_stock(self, stock):
        cost = stock.get("price", 0) * stock.get("quantity", 0)
        if self.cash_balance < cost:
            return False
        self.add_stock(stock)
        self.cash_balance -= cost
        return True

    def sell_stock(self, stock):
        if not self.remove_stock(stock):
            return False
        proceeds = stock.get("price", 0) * stock.get("quantity", 0)
        self.cash_balance += proceeds
        return True

    def get_stock_value(self, stock):
        return stock.get("price", 0) * stock.get("quantity", 0)

    def calculate_portfolio_value(self):
        return self.cash_balance + sum(self.get_stock_value(stock) for stock in self.portfolio)

    def get_portfolio_summary(self):
        summary = [{"name": stock.get("name"), "value": self.get_stock_value(stock)} for stock in self.portfolio]
        return self.calculate_portfolio_value(), summary

import unittest

class StockPortfolioTrackerTestGetPortfolioSummary(unittest.TestCase):
    def test_get_portfolio_summary(self):
        tracker = StockPortfolioTracker(10000.0)
        tracker.portfolio = [{'name': 'AAPL', 'price': 150.0, 'quantity': 10}]
        self.assertEqual(tracker.get_portfolio_summary(), (11500.0, [{'name': 'AAPL', 'value': 1500.0}]))

    def test_get_portfolio_summary_2(self):
        tracker = StockPortfolioTracker(10000.0)
        tracker.portfolio = [{'name': 'AAPL', 'price': 150.0, 'quantity': 10},
                             {'name': 'MSFT', 'price': 150.0, 'quantity': 10}]
        self.assertEqual(tracker.get_portfolio_summary(),
                         (13000.0, [{'name': 'AAPL', 'value': 1500.0}, {'name': 'MSFT', 'value': 1500.0}]))

    def test_get_portfolio_summary_3(self):
        tracker = StockPortfolioTracker(10000.0)
        self.assertEqual(tracker.get_portfolio_summary(), (10000.0, []))

    def test_get_portfolio_summary_4(self):
        tracker = StockPortfolioTracker(10000.0)
        tracker.portfolio = [{'name': 'AAPL', 'price': 150.0, 'quantity': 0}]
        self.assertEqual(tracker.get_portfolio_summary(), (10000.0, [{'name': 'AAPL', 'value': 0.0}]))

    def test_get_portfolio_summary_5(self):
        tracker = StockPortfolioTracker(10000.0)
        tracker.portfolio = [{'name': 'AAPL', 'price': 0.0, 'quantity': 10}]
        self.assertEqual(tracker.get_portfolio_summary(), (10000.0, [{'name': 'AAPL', 'value': 0.0}]))

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
