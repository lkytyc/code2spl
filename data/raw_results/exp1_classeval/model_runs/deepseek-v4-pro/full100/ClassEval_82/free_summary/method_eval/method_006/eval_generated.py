class StockPortfolioTracker:
    def __init__(self, initial_cash):
        self.cash = initial_cash
        self.portfolio = []

    def add_stock(self, name, price, quantity):
        for stock in self.portfolio:
            if stock['name'] == name:
                stock['quantity'] += quantity
                return True
        self.portfolio.append({'name': name, 'price': price, 'quantity': quantity})
        return True

    def remove_stock(self, name, quantity):
        for stock in self.portfolio:
            if stock['name'] == name:
                if stock['quantity'] >= quantity:
                    stock['quantity'] -= quantity
                    if stock['quantity'] == 0:
                        self.portfolio.remove(stock)
                    return True
                else:
                    return False
        return False

    def buy_stock(self, name, price, quantity):
        cost = price * quantity
        if self.cash >= cost:
            self.add_stock(name, price, quantity)
            self.cash -= cost
            return True
        return False

    def sell_stock(self, name, price, quantity):
        if self.remove_stock(name, quantity):
            self.cash += price * quantity
            return True
        return False

    def calculate_portfolio_value(self):
        total = self.cash
        for stock in self.portfolio:
            total += stock['price'] * stock['quantity']
        return total

    def get_stock_value(self, stock):
        return stock['price'] * stock['quantity']

    def get_portfolio_summary(self):
        total_value = self.calculate_portfolio_value()
        summary = []
        for stock in self.portfolio:
            summary.append({
                'name': stock['name'],
                'value': self.get_stock_value(stock)
            })
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
