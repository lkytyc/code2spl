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

class DiscountStrategyTestLargeOrderPromo(unittest.TestCase):
    def test_large_order_promo_1(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': f'product{i}', 'quantity': 1, 'price': 10.0} for i in range(10)]
        order = DiscountStrategy(customer, cart, DiscountStrategy.LargeOrderPromo)
        expected_discount = 7.0
        actual_discount = order.promotion(order)
        self.assertAlmostEqual(actual_discount, expected_discount)

    def test_large_order_promo_2(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': f'product{i}', 'quantity': 1, 'price': 10.0} for i in range(5)]
        order = DiscountStrategy(customer, cart, DiscountStrategy.LargeOrderPromo)
        expected_discount = 0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_large_order_promo_3(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': f'product{i}', 'quantity': 1, 'price': 10.0} for i in range(100)]
        order = DiscountStrategy(customer, cart, DiscountStrategy.LargeOrderPromo)
        expected_discount = 70.0
        actual_discount = order.promotion(order)
        self.assertAlmostEqual(actual_discount, expected_discount)

    def test_large_order_promo_4(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': f'product{i}', 'quantity': 1, 'price': 10.0} for i in range(1000)]
        order = DiscountStrategy(customer, cart, DiscountStrategy.LargeOrderPromo)
        expected_discount = 700.0
        actual_discount = order.promotion(order)
        self.assertAlmostEqual(actual_discount, expected_discount)

    def test_large_order_promo_5(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': f'product{i}', 'quantity': 1, 'price': 10.0} for i in range(1)]
        order = DiscountStrategy(customer, cart, DiscountStrategy.LargeOrderPromo)
        expected_discount = 0.0
        actual_discount = order.promotion(order)
        self.assertAlmostEqual(actual_discount, expected_discount)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
