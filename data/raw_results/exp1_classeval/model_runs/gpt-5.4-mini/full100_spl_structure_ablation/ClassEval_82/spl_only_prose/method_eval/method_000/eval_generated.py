class StockPortfolioTracker:
    def __init__(self, cash_balance):
        self.portfolio = []
        self.cash_balance = cash_balance

    def add_stock(self, stock: dict):
        for pf in self.portfolio:
            name_match = pf.get('name') == stock.get('name')
            if name_match:
                pf['quantity'] += stock.get('quantity', 0)
                return
        self.portfolio.append(stock)

    def buy_stock(self, stock: dict) -> bool:
        purchase_cost = stock['price'] * stock['quantity']
        is_too_expensive = purchase_cost > self.cash_balance
        if is_too_expensive:
            return False
        self.add_stock(stock)
        self.cash_balance -= purchase_cost
        return True

    def calculate_portfolio_value(self):
        total_value = self.cash_balance
        for stock in self.portfolio:
            total_value += stock['price'] * stock['quantity']
        return total_value

    def get_portfolio_summary(self):
        summary = []
        for stock in self.portfolio:
            summary.append({
                'name': stock['name'],
                'value': self.get_stock_value(stock)
            })
        portfolio_value = self.calculate_portfolio_value()
        return portfolio_value, summary

    def get_stock_value(self, stock: dict):
        price_and_quantity = (stock['price'], stock['quantity'])
        result = price_and_quantity[0] * price_and_quantity[1]
        return result

    def remove_stock(self, stock: dict) -> bool:
        for pf in self.portfolio:
            match_and_sufficient_quantity = pf['name'] == stock['name'] and pf['quantity'] >= stock['quantity']
            if match_and_sufficient_quantity:
                pf['quantity'] -= stock['quantity']
                if pf['quantity'] == 0:
                    self.portfolio.remove(pf)
                return True
        return False

    def sell_stock(self, stock: dict) -> bool:
        removal_failed = self.remove_stock(stock) == False
        if removal_failed:
            return False
        self.cash_balance += stock['price'] * stock['quantity']
        return True

import unittest

class StockPortfolioTrackerTestAddStock(unittest.TestCase):
    def test_add_stock(self):
        tracker = StockPortfolioTracker(10000.0)
        tracker.add_stock({"name": "AAPL", "price": 150.0, "quantity": 10})
        self.assertEqual(tracker.portfolio, [{'name': 'AAPL', 'price': 150.0, 'quantity': 10}])

    def test_add_stock_2(self):
        tracker = StockPortfolioTracker(10000.0)
        tracker.portfolio = [{'name': 'AAPL', 'price': 150.0, 'quantity': 10}]
        tracker.add_stock({"name": "AAPL", "price": 150.0, "quantity": 10})
        self.assertEqual(tracker.portfolio, [{'name': 'AAPL', 'price': 150.0, 'quantity': 20}])

    def test_add_stock_3(self):
        tracker = StockPortfolioTracker(10000.0)
        tracker.portfolio = [{'name': 'AAPL', 'price': 150.0, 'quantity': 10}]
        tracker.add_stock({"name": "MSFT", "price": 150.0, "quantity": 10})
        self.assertEqual(tracker.portfolio, [{'name': 'AAPL', 'price': 150.0, 'quantity': 10},
                                             {'name': 'MSFT', 'price': 150.0, 'quantity': 10}])

    def test_add_stock_4(self):
        tracker = StockPortfolioTracker(10000.0)
        tracker.portfolio = [{'name': 'AAPL', 'price': 150.0, 'quantity': 10}]
        tracker.add_stock({"name": "AAPL", "price": 150.0, "quantity": 10})
        tracker.add_stock({"name": "MSFT", "price": 150.0, "quantity": 10})
        self.assertEqual(tracker.portfolio, [{'name': 'AAPL', 'price': 150.0, 'quantity': 20},
                                             {'name': 'MSFT', 'price': 150.0, 'quantity': 10}])

    def test_add_stock_5(self):
        tracker = StockPortfolioTracker(10000.0)
        tracker.portfolio = [{'name': 'AAPL', 'price': 150.0, 'quantity': 10}]
        tracker.add_stock({"name": "AAPL", "price": 150.0, "quantity": 10})
        tracker.add_stock({"name": "MSFT", "price": 150.0, "quantity": 10})
        tracker.add_stock({"name": "MSFT", "price": 150.0, "quantity": 10})
        self.assertEqual(tracker.portfolio, [{'name': 'AAPL', 'price': 150.0, 'quantity': 20},
                                             {'name': 'MSFT', 'price': 150.0, 'quantity': 20}])

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
