class DiscountStrategy:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion
        self.__total = self.total()

    def BulkItemPromo(self, order):
        discount = 0
        for item in order.cart:
            if item['quantity'] >= 20:
                discount += item['quantity'] * item['price'] * 0.1
        return discount

    def FidelityPromo(self, order):
        fidelity = order.customer['fidelity']
        is_eligible = fidelity >= 1000
        if is_eligible:
            discount = order.total() * 0.05
            return discount
        return 0

    def LargeOrderPromo(self, order):
        distinct_products = {item['product'] for item in order.cart}
        distinct_product_count = len(distinct_products)
        if distinct_product_count >= 10:
            return order.total() * 0.07
        return 0

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.__total - discount

    def total(self):
        self.__total = sum(item['quantity'] * item['price'] for item in self.cart)
        return self.__total

import unittest

class DiscountStrategyTestFidelityPromo(unittest.TestCase):
    def test_fidelity_promo_1(self):
        customer = {'name': 'John Doe', 'fidelity': 1000}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        expected_discount = 12.5
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_fidelity_promo_2(self):
        customer = {'name': 'John Doe', 'fidelity': 800}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        expected_discount = 0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_fidelity_promo_3(self):
        customer = {'name': 'John Doe', 'fidelity': 0}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        expected_discount = 0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_fidelity_promo_4(self):
        customer = {'name': 'John Doe', 'fidelity': 10000}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        expected_discount = 12.5
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_fidelity_promo_5(self):
        customer = {'name': 'John Doe', 'fidelity': 1800}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 20.0},
                {'product': 'product2', 'quantity': 5, 'price': 10.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.FidelityPromo)
        expected_discount = 12.5
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
