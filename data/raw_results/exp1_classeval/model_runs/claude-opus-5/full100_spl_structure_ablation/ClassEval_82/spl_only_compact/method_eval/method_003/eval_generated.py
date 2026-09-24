class StockPortfolioTracker:
    def __init__(self, cash_balance):
        self.portfolio = []
        self.cash_balance = cash_balance

    def add_stock(self, stock):
        for pf in self.portfolio:
            if pf['name'] == stock['name']:
                pf['quantity'] += stock['quantity']
                return
        self.portfolio.append(stock)

    def buy_stock(self, stock):
        total_cost = stock['price'] * stock['quantity']
        if total_cost > self.cash_balance:
            return False
        self.add_stock(stock)
        self.cash_balance -= total_cost
        return True

    def calculate_portfolio_value(self):
        total_value = self.cash_balance
        for stock in self.portfolio:
            total_value += stock['price'] * stock['quantity']
        return total_value

    def get_portfolio_summary(self):
        summary = []
        for stock in self.portfolio:
            value = self.get_stock_value(stock)
            summary.append({'name': stock['name'], 'value': value})
        portfolio_value = self.calculate_portfolio_value()
        return (portfolio_value, summary)

    def get_stock_value(self, stock):
        return stock['price'] * stock['quantity']

    def remove_stock(self, stock):
        for pf in self.portfolio:
            if pf['name'] == stock['name'] and pf['quantity'] >= stock['quantity']:
                pf['quantity'] -= stock['quantity']
                if pf['quantity'] == 0:
                    self.portfolio.remove(pf)
                return True
        return False

    def sell_stock(self, stock):
        if self.remove_stock(stock) == False:
            return False
        sale_proceeds = stock['price'] * stock['quantity']
        self.cash_balance += sale_proceeds
        return True

import unittest

class StockPortfolioTrackerTestSellStock(unittest.TestCase):
    def test_sell_stock(self):
        tracker = StockPortfolioTracker(10000.0)
        tracker.portfolio = [{'name': 'AAPL', 'price': 150.0, 'quantity': 10}]
        self.assertEqual(tracker.sell_stock({"name": "AAPL", "price": 150.0, "quantity": 9}), True)
        self.assertEqual(tracker.portfolio, [{"name": "AAPL", "price": 150.0, "quantity": 1}])
        self.assertEqual(tracker.cash_balance, 11350.0)

    def test_sell_stock_2(self):
        tracker = StockPortfolioTracker(10000.0)
        tracker.portfolio = [{'name': 'AAPL', 'price': 150.0, 'quantity': 10}]
        self.assertEqual(tracker.sell_stock({"name": "AAPL", "price": 150.0, "quantity": 20}), False)
        self.assertEqual(tracker.portfolio, [{"name": "AAPL", "price": 150.0, "quantity": 10}])
        self.assertEqual(tracker.cash_balance, 10000.0)

    def test_sell_stock_3(self):
        tracker = StockPortfolioTracker(10000.0)
        self.assertEqual(tracker.sell_stock({"name": "AAPL", "price": 150.0, "quantity": 10}), False)
        self.assertEqual(tracker.portfolio, [])
        self.assertEqual(tracker.cash_balance, 10000.0)

    def test_sell_stock_4(self):
        tracker = StockPortfolioTracker(10000.0)
        tracker.portfolio = [{'name': 'AAPL', 'price': 150.0, 'quantity': 20}]
        self.assertEqual(tracker.sell_stock({"name": "AAPL", "price": 150.0, "quantity": 20}), True)
        self.assertEqual(tracker.portfolio, [])
        self.assertEqual(tracker.cash_balance, 13000.0)

    def test_sell_stock_5(self):
        tracker = StockPortfolioTracker(10000.0)
        tracker.portfolio = [{'name': 'AAPL', 'price': 150.0, 'quantity': 20},
                             {'name': 'MSFT', 'price': 150.0, 'quantity': 10}]
        self.assertEqual(tracker.sell_stock({"name": "AAPL", "price": 150.0, "quantity": 20}), True)
        self.assertEqual(tracker.portfolio, [{'name': 'MSFT', 'price': 150.0, 'quantity': 10}])
        self.assertEqual(tracker.cash_balance, 13000.0)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
