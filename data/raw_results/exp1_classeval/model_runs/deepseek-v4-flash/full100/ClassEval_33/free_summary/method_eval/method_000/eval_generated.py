class DiscountStrategy:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion

    def total(self):
        self._total = sum(item["quantity"] * item["price"] for item in self.cart)
        return self._total

    def due(self):
        total = self.total()
        if self.promotion is None:
            return total
        return total - self.promotion(self)

    @staticmethod
    def FidelityPromo(order):
        if order.customer.fidelity >= 1000:
            return 0.05 * order.total()
        return 0.0

    @staticmethod
    def BulkItemPromo(order):
        return sum(
            0.1 * item["quantity"] * item["price"]
            for item in order.cart
            if item["quantity"] >= 20
        )

    @staticmethod
    def LargeOrderPromo(order):
        if len({item["product"] for item in order.cart}) >= 10:
            return 0.07 * order.total()
        return 0.0

import unittest

class DiscountStrategyTestTotal(unittest.TestCase):
    def test_total_1(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart)
        expected_total = 250.0
        actual_total = order.total()
        self.assertEqual(actual_total, expected_total)

    def test_total_2(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 10.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart)
        expected_total = 150.0
        actual_total = order.total()
        self.assertEqual(actual_total, expected_total)

    def test_total_3(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 200.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart)
        expected_total = 2050.0
        actual_total = order.total()
        self.assertEqual(actual_total, expected_total)

    def test_total_4(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 1, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart)
        expected_total = 70.0
        actual_total = order.total()
        self.assertEqual(actual_total, expected_total)

    def test_total_5(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = []
        order = DiscountStrategy(customer, cart)
        expected_total = 0
        actual_total = order.total()
        self.assertEqual(actual_total, expected_total)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
