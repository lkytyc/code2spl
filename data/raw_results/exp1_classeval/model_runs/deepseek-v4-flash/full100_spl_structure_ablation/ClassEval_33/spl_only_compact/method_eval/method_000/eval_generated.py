class DiscountStrategy:
    def __init__(self, customer: object, cart: object, promotion: object = None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion
        self.__total = self.total()

    @staticmethod
    def BulkItemPromo(order: object) -> float:
        discount = 0
        for item in order.cart:
            if item['quantity'] >= 20:
                discount += item['quantity'] * item['price'] * 0.1
        return discount

    @staticmethod
    def FidelityPromo(order: object) -> float:
        if order.customer['fidelity'] >= 1000:
            promo_value = order.total() * 0.05
        else:
            promo_value = 0
        return promo_value

    @staticmethod
    def LargeOrderPromo(order: object) -> float:
        distinct_products = {item['product'] for item in order.cart}
        if len(distinct_products) >= 10:
            return order.total() * 0.07
        else:
            return 0

    def due(self) -> float:
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.__total - discount

    def total(self) -> float:
        self.__total = sum(item['quantity'] * item['price'] for item in self.cart)
        return self.__total

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
