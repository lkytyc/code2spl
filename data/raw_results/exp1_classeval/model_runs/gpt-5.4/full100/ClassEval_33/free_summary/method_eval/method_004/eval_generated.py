class DiscountStrategy:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion
        self.__total = 0
        self.total()

    def total(self):
        self.__total = sum(item['quantity'] * item['price'] for item in self.cart)
        return self.__total

    def due(self):
        discount = 0 if self.promotion is None else self.promotion(self)
        return self.__total - discount

    @staticmethod
    def FidelityPromo(order):
        if order.customer.get('fidelity', 0) >= 1000:
            return order.total() * 0.05
        return 0

    @staticmethod
    def BulkItemPromo(order):
        discount = 0
        for item in order.cart:
            if item['quantity'] >= 20:
                discount += item['quantity'] * item['price'] * 0.10
        return discount

    @staticmethod
    def LargeOrderPromo(order):
        distinct_items = {item.get('product') for item in order.cart if 'product' in item}
        if len(distinct_items) >= 10:
            return order.total() * 0.07
        return 0

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
