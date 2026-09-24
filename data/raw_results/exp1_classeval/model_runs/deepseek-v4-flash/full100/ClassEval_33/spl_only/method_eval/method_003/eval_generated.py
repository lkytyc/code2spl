class DiscountStrategy:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion
        self.__total = self.total()

    def total(self):
        self.__total = sum(item['quantity'] * item['price'] for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.__total - discount

    @staticmethod
    def FidelityPromo(order):
        if order.customer['fidelity'] >= 1000:
            promo_value = order.total() * 0.05
        else:
            promo_value = 0
        return promo_value

    @staticmethod
    def BulkItemPromo(order):
        discount = 0
        for item in order.cart:
            if item['quantity'] >= 20:
                discount += item['quantity'] * item['price'] * 0.1
        return discount

    @staticmethod
    def LargeOrderPromo(order):
        distinct_products = {item['product'] for item in order.cart}
        if len(distinct_products) >= 10:
            return order.total() * 0.07
        else:
            return 0

import unittest

class DiscountStrategyTestBulkItemPromo(unittest.TestCase):
    def test_bulk_item_promo_1(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 20, 'price': 10.0},
                {'product': 'product2', 'quantity': 5, 'price': 5.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.BulkItemPromo)
        expected_discount = 20.0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_bulk_item_promo_2(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 10, 'price': 10.0},
                {'product': 'product2', 'quantity': 5, 'price': 5.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.BulkItemPromo)
        expected_discount = 0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_bulk_item_promo_3(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 100, 'price': 10.0},
                {'product': 'product2', 'quantity': 5, 'price': 5.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.BulkItemPromo)
        expected_discount = 100.0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_bulk_item_promo_4(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 1, 'price': 10.0},
                {'product': 'product2', 'quantity': 5, 'price': 5.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.BulkItemPromo)
        expected_discount = 0.0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

    def test_bulk_item_promo_5(self):
        customer = {'name': 'John Doe', 'fidelity': 1200}
        cart = [{'product': 'product1', 'quantity': 30, 'price': 10.0},
                {'product': 'product2', 'quantity': 5, 'price': 5.0}]
        order = DiscountStrategy(customer, cart, DiscountStrategy.BulkItemPromo)
        expected_discount = 30.0
        actual_discount = order.promotion(order)
        self.assertEqual(actual_discount, expected_discount)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
